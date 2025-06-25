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
    client=client,
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
        # create ui
        ui = smolagents.GradioUI(
            agent, file_upload_folder="uploads", reset_agent_memory=False
        )
        ui.launch()
