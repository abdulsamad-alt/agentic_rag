import streamlit as st
from core.agent import AgentSystem

st.set_page_config(page_title="Agentic RAG Bot", layout="centered")
st.title("🤖 Pure Agentic RAG")

if "agent" not in st.session_state:
    st.session_state.agent = AgentSystem()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask about the document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.agent.run(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})