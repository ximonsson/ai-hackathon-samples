import pathlib
from typing import Annotated
from typing_extensions import TypedDict
import databricks.sdk
import langchain.chat_models
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import langchain_unstructured
import torch
import streamlit as st


MODEL = "data-science-gpt-4o"
MODEL_EMB = "sentence-transformers/all-MiniLM-L6-v2"
DOC = "harry-potter-and-the-sorcerers-stone.pdf"

embedder = HuggingFaceEmbeddings(
    model_name=MODEL_EMB,
    model_kwargs={
        "model_kwargs": {"torch_dtype": torch.float16}
    },  # half precision for faster inference
    encode_kwargs={"normalize_embeddings": False, "batch_size": 16},
    show_progress=True,
)

# get databricks workspace client and fetch the OpenAI client towards
# serving endpoints.
wc = databricks.sdk.WorkspaceClient()
client = wc.serving_endpoints.get_open_ai_client()


def create_index(doc: str):
    # load document and chunk it
    # this function should support quite a lot of different file formats
    ld = langchain_unstructured.UnstructuredLoader(doc)
    chunks = ld.load_and_split()

    # filter out only narrative text to index and create index
    chunks = list(filter(lambda x: x.metadata["category"] == "NarrativeText", chunks))
    idx = FAISS.from_documents(chunks, embedder)

    return idx


def search_index(idx, q: str, topk: int = 50):
    """
    Search the index for the query and return the topk results.
    """
    retriever = idx.as_retriever(search_kwargs={"k": topk})
    docs = retriever.invoke(q)
    return docs


def graph(idx) -> StateGraph:
    """
    return graph
    """

    #
    # Setup LLM
    #

    # read system prompt for the agent
    with open(pathlib.Path(__file__).parent / "sysprompt.txt") as f:
        prompt = f.read()

    def search(q: str) -> str:
        """
        Search the document for relevant chunks to query.

        Args:
            q (str): Query.

        Returns:
            str: All relevant chunks delimited by "\n\n=======\n\n".
        """
        docs = search_index(idx, q)
        return "\n\n=======\n\n".join([x.page_content for x in docs])

    # the agent will have as a tool to be able to search the document
    tool = search
    llm = langchain.chat_models.init_chat_model(
        f"openai:{MODEL}",
        base_url=str(client.base_url),
        temperature=0.1,
    ).bind_tools([tool])

    #
    # Setup graph
    #

    # define custom class that keeps track of the state
    class State(TypedDict):
        query: str
        messages: Annotated[list, add_messages]

    # Node handling interaction with the LLM
    def chatbot(state: State):
        return {
            "query": state["query"],
            "messages": [llm.invoke(state["messages"])],
        }

    # Node for invoking tools
    tool_node = ToolNode(tools=[tool])

    # create system prompt template
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", prompt),
            ("human", "{input}"),
        ]
    )

    def sysprompt(state: State):
        # NOTE we blindly start from zero here
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

    return graph


def main() -> None:
    idx = create_index(DOC)
    g = graph(idx)
    print(g.invoke({"query": "what happened to harry's parents?"}))
