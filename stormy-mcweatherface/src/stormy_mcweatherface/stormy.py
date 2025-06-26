import json
from typing import Any, Callable, Generator, Optional, Dict
import os
import sys
from uuid import uuid4
import asyncio
import httpx

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
#from stormy_mcweatherface import get_geocode_location, get_weather


async def get_geocode_location(query: str, limit: int = 1) -> Optional[Dict[str, Any]]:
    """
    Geocode a location using the Nominatim API.
    
    Args:
        query: The location to search for (e.g., "Paris, France")
        limit: Maximum number of results to return (default: 1)
    
    Returns:
        Dictionary containing the geocoding result or None if not found
    """
    base_url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        "q": query,
        "format": "json",
        "limit": limit,
        "addressdetails": 1
    }
    
    headers = {
        "User-Agent": "stormy-mcweatherface/0.1.0"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            
            results = response.json()
            if results:
                return {
                "success": True,
                "location": results[0].get('display_name', query),
                "latitude": float(results[0]['lat']),
                "longitude": float(results[0]['lon'])
            } 

            #return results[0] if results else None
            else:
                return {
                    "success": False,
                    "error": f"Could not find coordinates for location: {query}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error geocoding location: {str(e)}"
            }



async def get_weather(lat, lon, user_agent="MyApp/1.0 (oda.johanne.kristensen[at]posten.no)"):
    """
    Get weather forecast from met.no API
    
    Args:
        lat: Latitude
        lon: Longitude  
        user_agent: Your app name and contact info (REQUIRED)
    
    Returns:
        Weather data dictionary or None if failed
    """
    # Round coordinates to 4 decimals (API requirement)
    lat = round(lat, 4)
    lon = round(lon, 4)
    
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    
    headers = {
        'User-Agent': user_agent
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
        
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print("Error: Invalid User-Agent. Please use your real app name and contact info.")
            elif response.status_code == 429:
                print("Error: Too many requests. Please wait before trying again.")
            else:
                print(f"Error: HTTP {response.status_code}")
                
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None


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
            temperature=1.2
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

tools = [
    ToolInfo(
        name="get_geocode_location",
        spec={
            "type": "function", 
            "function": {
            "name": "get_geocode_location", 
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
        exec_fn=lambda location: asyncio.run(get_geocode_location(location))
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
        exec_fn=lambda lat, lon: asyncio.run(get_weather(float(lat), float(lon)))
    )
]

SYSTEM_PROMPT = "You are Stormy McWeatherface, a helpful location assistant. When users provides a location, use the get_location_coordinates tool to find the GPS coordinates, and then send those coordinates to get_location_weather, and present the current weather for the requested location, together with the locations gps coordinates, in a friendly, conversational way. Give suggestions of activities that will suit the current weather conditions"

mlflow.openai.autolog()
AGENT = ToolCallingAgent(model="data-science-gpt-4o", tools=tools)
mlflow.models.set_model(AGENT)