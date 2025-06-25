import pathlib
import os
from typing import Annotated
from typing_extensions import TypedDict
import databricks.sdk

# from langchain_community.tools import DuckDuckGoSearchResults
import langchain.chat_models
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.prompts import ChatPromptTemplate
import faiss
import sentence_transformers
import langchain_unstructured


wc = databricks.sdk.WorkspaceClient()
client = wc.serving_endpoints.get_open_ai_client()

MODEL = "data-science-gpt-4o"
MODEL_EMB = "sentence-transformers/all-MiniLM-L6-v2"
DOC = "harry-potter-and-the-sorcerers-stone.pdf"

embedder = sentence_transformers.SentenceTransformer(MODEL_EMB)

#
# index the document
#


def create_index():
    ld = langchain_unstructured.UnstructuredLoader(DOC)
    doc = ld.load()
    return doc


def search_index(topk: int = 50):
    """ """
    pass


#
# Create graph
#


# read system prompt for the agent

with open(pathlib.Path(__file__).parent / "sysprompt.txt") as f:
    prompt = f.read()


class State(TypedDict):
    query: str
    messages: Annotated[list, add_messages]


# TODO these search results are no good, I would like the same as smolagents
# tool = DuckDuckGoSearchResults(max_results=10)

tool = search_index
llm = langchain.chat_models.init_chat_model(
    f"openai:{MODEL}",
    base_url=str(client.base_url),
    temperature=0.1,
).bind_tools([tool])


def chatbot(state: State):
    return {
        "query": state["query"],
        "messages": [llm.invoke(state["messages"])],
    }


tool_node = ToolNode(tools=[tool])

# create system prompt template

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", prompt),
        ("human", "{input}"),
    ]
)


def sysprompt(state: State):
    return {
        "query": state["query"],
        "messages": prompt_template.invoke({"input": state["query"]}).messages,
    }


# create graph

graph_builder = StateGraph(State)

# nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("sysprompt", sysprompt)

# edges
graph_builder.add_edge(START, "sysprompt")
graph_builder.add_edge("sysprompt", "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()


def main() -> None:
    pass
