import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="MCP AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 MCP AI Assistant")
st.caption("Chat with umer's AI tool-powered assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input (like ChatGPT style)
if prompt := st.chat_input("Type your message here..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{API_URL}/chat",
                json={"messages": st.session_state.messages}
            )
            reply = response.json()["response"]
            st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
