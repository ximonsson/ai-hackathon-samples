import mlflow
from mlflow.types.responses import ResponsesAgentRequest
from . import stormy
import sys

def main():
    # Get location from command line argument or use default
    if len(sys.argv) > 1:
        location = " ".join(sys.argv[1:])  # Join all arguments in case of spaces
    else:
        location = "Biskop Gunnerus gate 14"
    
    print(f"🌦️ Getting weather information for: {location}")
    
    request = ResponsesAgentRequest(
        input=[
            {
                "role": "user",
                "content": f"What is the weather like in {location}?"
            }
        ]
    )
    mlflow.openai.autolog()
    agent = stormy.create_agent()
    response = agent.predict(request)
    print("\n🤖 Stormy McWeatherface:")
    for output in response.output:
        if output.type == 'message':
            content = output.content
            if content:
                print(content[0].get('text', ''))
        elif 'content' in output:
            print(output['content'])