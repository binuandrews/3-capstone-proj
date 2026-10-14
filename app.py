import warnings
from idlelib import history

warnings.filterwarnings("ignore")

import streamlit as st
from llm_providers import run_llm

st.set_page_config(page_title="LLM Conversation", layout="wide", page_icon="🤖")
st.title("LLM Conversation")

# History of the conversation
if "history" not in st.session_state:
    st.session_state['history'] = [
      {
        "role": "assistant",
        "content": "Hello! I'm your AI assistant. How can I help you today?"
      }
    ]

# Display the conversation history
for msg in st.session_state["history"]:
  st.chat_message(msg["role"]).markdown(msg["content"])
