import smolagents
import databricks.sdk
import mcp
import os

MODEL = "data-science-gpt-4o"

wc = databricks.sdk.WorkspaceClient()
client = wc.serving_endpoints.get_open_ai_client()

# create a smolagents agent
model = smolagents.OpenAIServerModel(
    model_id=MODEL,
    api_base=client.base_url,
)

params = mcp.StdioServerParameters(
    command="docker",
    args=[
        "run",
        "-i",
        "--rm",
        "-e",
        f"GITHUB_PERSONAL_ACCESS_TOKEN={os.environ['GITHUB_PERSONAL_ACCESS_TOKEN']}",
        "ghcr.io/github/github-mcp-server",
    ],
)


def main() -> None:
    with smolagents.ToolCollection.from_mcp(
        params, trust_remote_code=True
    ) as tool_collection:
        agent = smolagents.ToolCallingAgent(
            tools=[*tool_collection.tools], model=model, add_base_tools=False
        )
        agent.run("how many open pull requests does bring/iac-ekofisk have?")
