import gradio as gr
import mlflow
import asyncio
import signal
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from mlflow.types.responses import ResponsesAgentRequest
from . import stormy


def get_weather_response(location: str) -> str:
    """Get weather response from the agent for a given location"""
    if not location.strip():
        return "Please enter a location!"
    
    try:
        # Create the agent
        mlflow.openai.autolog()
        agent = stormy.create_agent()
        
        # Create request
        request = ResponsesAgentRequest(
            input=[
                {
                    "role": "user",
                    "content": f"What is the weather like in {location}?"
                }
            ]
        )
        
        # Get response from agent
        response = agent.predict(request)
        
        # Extract text from response

        for output in response.output:
            if output.type == 'message':
                content = output.content
                if content:
                    result = content[0].get('text', '')
            elif 'content' in output:
                result = output['content']

        
        return result if result else "I couldn't get a response from the agent."
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


def create_gradio_interface():
    """Create and configure the Gradio interface"""
    
    # Create the interface
    interface = gr.Interface(
        fn=get_weather_response,
        inputs=[
            gr.Textbox(
                label="Location",
                placeholder="Enter a location (e.g., 'Oslo, Norway', 'Paris, France')",
                value="Biskop Gunnerus gate 14"
            )
        ],
        outputs=[
            gr.Textbox(
                label="Weather Response",
                lines=10,
                max_lines=20
            )
        ],
        title="🌦️ Stormy McWeatherface",
        description="Get weather information for any location using AI-powered location lookup and weather forecasting.",
        examples=[
            ["Alfasetveien 24"],
            ["Posthuset, Oslo"],
            ["Dette er et fint sted"],
            ["Biskop Gunnerus gate 14"],
            ["Østlandsterminalen"],
            ["Youngstorget 3"]
        ],
        theme=gr.themes.Soft(),
        flagging_mode="never"
    )
    
    return interface


def launch_app(share=False, debug=False):
    """Launch the Gradio app"""
    interface = create_gradio_interface()
    interface.launch(share=share, debug=debug)


if __name__ == "__main__":
    launch_app(share=True, debug=True)