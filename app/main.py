import sys
import os
# Auto-build index if not exists
if not os.path.exists("data/vector_db/index.faiss"):
    print("⚠️ Index not found. Building index...")

    from build_index import main as build_main
    build_main()

    print("✅ Index built successfully")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from core.agent import AgentSystem

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Agentic RAG", layout="wide")

st.title("HYBRID RAG BOOK Assistant")
st.markdown("Ask questions from your PDF (with images + memory)")

# -------------------------
# LOAD AGENT (ONCE)
# -------------------------
@st.cache_resource
def load_agent():
    return AgentSystem()

agent = load_agent()

# -------------------------
# SESSION STATE (CHAT)
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# DISPLAY CHAT HISTORY
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# USER INPUT
# -------------------------
user_input = st.chat_input("Ask something about your document...")

if user_input:
    # show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent.run(user_input)
            st.markdown(response)

    # save response
    st.session_state.messages.append({"role": "assistant", "content": response})