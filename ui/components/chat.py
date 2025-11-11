# ui/components/chat_component.py
import streamlit as st
import requests

def chat_component():
    st.subheader("💬 Chat with the AI Code Agent")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Type your message", key="user_input")

    if st.button("Send"):
        if user_input.strip():
            st.session_state.chat_history.append(("🧑‍💻 You", user_input))

            with st.spinner("Thinking..."):
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"query": user_input}
                )

            if response.status_code == 200:
                bot_reply = response.json().get("response", "No response")
                st.session_state.chat_history.append(("🤖 AI Agent", bot_reply))
            else:
                st.error("Failed to get response from the agent.")
    
    # Display conversation history
    for sender, msg in st.session_state.chat_history:
        st.markdown(f"**{sender}:** {msg}")
