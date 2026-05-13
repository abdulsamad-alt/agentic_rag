import streamlit as st
import sys
import os

# --- ADD THIS TO FIX THE MODULE NOT FOUND ERROR ---
# This adds the parent directory (project root) to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from core.agent import AgentSystem
except ImportError as e:
    st.error(f"Error importing core.agent: {e}")
    st.stop()
# --------------------------------------------------

st.set_page_config(page_title="Agentic RAG Bot", layout="centered")
st.title("🤖 Pure Agentic RAG")

# Check for API Key in Streamlit Secrets (for deployment) or Environment
from core.config import GEMINI_API_KEY
if not GEMINI_API_KEY:
    st.error("Missing Gemini API Key. Please add it to your secrets or .env file.")
    st.stop()

if "agent" not in st.session_state:
    with st.spinner("Initializing Agentic Brain..."):
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
        with st.spinner("Thinking..."):
            response = st.session_state.agent.run(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})