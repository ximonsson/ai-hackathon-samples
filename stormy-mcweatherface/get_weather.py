import json
from typing import Any, Callable, Generator
import os
from uuid import uuid4
import asyncio

import backoff
import mlflow
import openai
from mlflow.entities import SpanType
from mlflow.pyfunc import ResponsesAgent
from mlflow.types.responses import (
    ResponsesAgentRequest,
    ResponsesAgentResponse,
    ResponsesAgentStreamEvent,
)
from pydantic import BaseModel

import databricks.sdk
from stormy_mcweatherface import geocode_location, get_weather



class ToolInfo(BaseModel):
    """
    Class representing a tool for the agent.
    - "name" (str): The name of the tool.
    - "spec" (dict): JSON description of the tool (matches OpenAI Responses format)
    - "exec_fn" (Callable): Function that implements the tool logic
    """

    name: str
    spec: dict
    exec_fn: Callable


class ToolCallingAgent(ResponsesAgent):
    """
    Class representing a tool-calling Agent
    """

    def __init__(self, model: str, tools: list[ToolInfo]):
        """Initializes the ToolCallingAgent with tools."""
        self.model = model
        self._tools_dict = {tool.name: tool for tool in tools}
        
        self.wc = databricks.sdk.WorkspaceClient()
        self.client = self.wc.serving_endpoints.get_open_ai_client()

    def get_tool_specs(self) -> list[dict]:
        """Returns tool specifications in the format OpenAI expects."""
        return [tool_info.spec for tool_info in self._tools_dict.values()]

    @mlflow.trace(span_type=SpanType.TOOL)
    def execute_tool(self, tool_name: str, args: dict) -> Any:
        """Executes the specified tool with the given arguments."""
        return self._tools_dict[tool_name].exec_fn(**args)

    @backoff.on_exception(backoff.expo, openai.RateLimitError)
    @mlflow.trace(span_type=SpanType.LLM)
    def call_llm(self, input_messages) -> ResponsesAgentStreamEvent:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=input_messages,
            tools=self.get_tool_specs(),
            temperature=0.7
        )
        
        message = response.choices[0].message
        if message.tool_calls:
            return {
                "id": str(uuid4()),
                "type": "function_call",
                "name": message.tool_calls[0].function.name,
                "call_id": message.tool_calls[0].id,
                "arguments": message.tool_calls[0].function.arguments,
                "role": "assistant",
                "content": message.content or "",
            }
        else:
            return {
                "id": str(uuid4()),
                "content": [{"type": "output_text", "text": message.content}],
                "role": "assistant",
                "type": "message",
            }

    def handle_tool_call(self, tool_call: dict[str, Any]) -> ResponsesAgentStreamEvent:
        """
        Execute tool calls and return a ResponsesAgentStreamEvent w/ tool output
        """
        args = json.loads(tool_call["arguments"])
        result = str(self.execute_tool(tool_name=tool_call["name"], args=args))

        tool_call_output = {
            "type": "function_call_output",
            "role": "function", 
            "name": tool_call["name"],
            "call_id": tool_call["call_id"],
            "content": result,
            "output": result,
        }
        return ResponsesAgentStreamEvent(
            type="response.output_item.done", item=tool_call_output
        )

    def call_and_run_tools(
        self,
        input_messages,
        max_iter: int = 10,
    ) -> Generator[ResponsesAgentStreamEvent, None, None]:
        for _ in range(max_iter):
            last_msg = input_messages[-1]
            if (
                last_msg.get("type", None) == "message"
                and last_msg.get("role", None) == "assistant"
            ):
                return
            if last_msg.get("type", None) == "function_call":
                tool_call_res = self.handle_tool_call(last_msg)
                input_messages.append(tool_call_res.item)
                yield tool_call_res
            else:
                llm_output = self.call_llm(input_messages=input_messages)
                input_messages.append(llm_output)
                yield ResponsesAgentStreamEvent(
                    type="response.output_item.done",
                    item=llm_output,
                )

        yield ResponsesAgentStreamEvent(
            type="response.output_item.done",
            item={
                "id": str(uuid4()),
                "content": [
                    {
                        "type": "output_text",
                        "text": "Max iterations reached. Stopping.",
                    }
                ],
                "role": "assistant",
                "type": "message",
            },
        )

    @mlflow.trace(span_type=SpanType.AGENT)
    def predict(self, request: ResponsesAgentRequest) -> ResponsesAgentResponse:
        outputs = [
            event.item
            for event in self.predict_stream(request)
            if event.type == "response.output_item.done"
        ]
        return ResponsesAgentResponse(
            output=outputs, custom_outputs=request.custom_inputs
        )

    @mlflow.trace(span_type=SpanType.AGENT)
    def predict_stream(
        self, request: ResponsesAgentRequest
    ) -> Generator[ResponsesAgentStreamEvent, None, None]:
        input_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
            i.model_dump() for i in request.input
        ]
        yield from self.call_and_run_tools(input_messages=input_messages)


# Tool implementation for getting GPS coordinates
async def get_coordinates_for_location(location: str) -> dict:
    """Get coordinates for a location using the geocode_location function"""
    try:
        result = await geocode_location(location)
        if result:
            return {
                "success": True,
                "location": result.get('display_name', location),
                "latitude": float(result['lat']),
                "longitude": float(result['lon'])
            }
        else:
            return {
                "success": False,
                "error": f"Could not find coordinates for location: {location}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error geocoding location: {str(e)}"
        }

tools = [
    ToolInfo(
        name="get_location_coordinates",
        spec={
            "type": "function",
            "function": {
            "name": "get_location_coordinates", 
            "description": "Get GPS coordinates (latitude and longitude) for a given location name or address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location name or address to get coordinates for (e.g., 'Paris, France', 'New York City', '1600 Pennsylvania Avenue')"
                    }
                },
                "required": ["location"],
                "additionalProperties": False,
            }},
            "strict": True,
        },
        exec_fn=lambda location: asyncio.run(get_coordinates_for_location(location))
    ), 
    ToolInfo(
        name="get_weather",
        spec={
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather information for a given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lat": {
                            "type": "string",
                            "description": "The latitude of the address to get weather for"
                        }, 
                        "lon": {
                            "type": "string",
                            "description": "The longitude of the address to get weather for"
                        }
                    },
                    "required": ["lat", "lon"],
                    "additionalProperties": False,
                }
            },
            "strict": True,
        },
        exec_fn=lambda lat, lon: get_weather(float(lat), float(lon))
    )
]

SYSTEM_PROMPT = "You are Stormy McWeatherface, a helpful location assistant. When users provides a location, use the get_location_coordinates tool to find the GPS coordinates, and then send those coordinates to get_location_weather, and present the current weather for the requested location, together with the locations gps coordinates, in a friendly, conversational way. Give a suggestion of what an activity that will suit the current weather conditions"

mlflow.openai.autolog()
AGENT = ToolCallingAgent(model="data-science-gpt-4o", tools=tools)
mlflow.models.set_model(AGENT)

# Test function to interact with the agent
def test_agent():
    request = ResponsesAgentRequest(
        input=[
            {
                "role": "system",
                 "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": "What is the weather like in Biskop Gunnerus gate 14?"
            }
        ]
    )
    
    response = AGENT.predict(request)
    print("Agent Response:")
    for output in response.output:
        if output.type == 'message':
            content = output.content
            if content:
                print(content[0].get('text', ''))
        elif 'content' in output:
            print(output['content'])

if __name__ == "__main__":
    test_agent()