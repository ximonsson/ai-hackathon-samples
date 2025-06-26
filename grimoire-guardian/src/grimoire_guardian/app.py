import streamlit as st
from grimoire_guardian import graph, create_index, DOC
import langchain_core

st.title("Grimoire Guardian")
st.markdown(f"Ask it anything about '{DOC}'")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


if "idx" not in st.session_state:
    with st.spinner("Indexing document..."):
        st.session_state.idx = create_index(DOC)
        st.success("Setup complete!")

g = graph(st.session_state.idx)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages = []
    # st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    res = g.invoke({"query": prompt})
    for m in langchain_core.messages.utils.convert_to_openai_messages(res["messages"]):
        if m["role"] in ["system", "user"]:
            continue

        with st.chat_message(m["role"]):
            if "tool_calls" in m:
                st.markdown(f"```\n{m['tool_calls']}\n```")
            if m["role"] == "tool":
                with st.expander("Tool results"):
                    st.markdown(m["content"])
            else:
                st.markdown(m["content"])
