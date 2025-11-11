# ui/app.py
import streamlit as st
from components.ticket_uploader import tickets_uploader_component
from components.chat import chat_component

st.set_page_config(page_title="AI Code Agent", layout="wide")

st.title("🤖 AI Code Agent")

tab1, tab2 = st.tabs(["📂 Upload Previous Tickets", "💬 Chat with Agent"])

with tab1:
    tickets_uploader_component()

with tab2:
    chat_component()
