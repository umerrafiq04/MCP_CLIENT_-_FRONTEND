import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000"

st.title("🤖 MCP AI Assistant")

# -----------------------
# SESSION STATE
# -----------------------

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "waiting_for_approval" not in st.session_state:
    st.session_state.waiting_for_approval = False


# -----------------------
# DISPLAY CHAT HISTORY
# -----------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -----------------------
# SINGLE INPUT BOX
# -----------------------

prompt = st.chat_input("Type your message...")


# -----------------------
# INPUT RECEIVED
# -----------------------

if prompt:

    # APPROVAL RESPONSE
    if st.session_state.waiting_for_approval:

        with st.chat_message("assistant"):

            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "resume": prompt,
                    "session_id": st.session_state.session_id,
                },
                stream=True,
            )

            text = ""

            for chunk in response.iter_content(1024, decode_unicode=True):
                if chunk:
                    text += chunk
                    st.markdown(text)

        st.session_state.messages.append(
            {"role": "assistant", "content": text}
        )

        st.session_state.waiting_for_approval = False


    # NORMAL MESSAGE
    else:

        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        # FIX: show user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "messages": st.session_state.messages,
                    "session_id": st.session_state.session_id,
                },
                stream=True,
            )

            text = ""

            for chunk in response.iter_content(1024, decode_unicode=True):

                if "__INTERRUPT__" in chunk:
                    st.session_state.waiting_for_approval = True
                    continue

                if "__END_INTERRUPT__" in chunk:
                    break

                text += chunk
                st.markdown(text)

        if not st.session_state.waiting_for_approval:
            st.session_state.messages.append(
                {"role": "assistant", "content": text}
            )
# wihtput hitl

# import streamlit as st
# import requests

# API_URL = "http://127.0.0.1:8000"

# st.set_page_config(
#     page_title="MCP AI Assistant",
#     page_icon="🤖",
#     layout="centered"
# )

# st.title("🤖 MCP AI Assistant")
# st.caption("Chat with umer's AI tool-powered assistant")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display previous messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Chat input (like ChatGPT style)
# if prompt := st.chat_input("Type your message here..."):

#     st.session_state.messages.append({
#         "role": "user",
#         "content": prompt
#     })

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):

#         def response_generator():
#             response = requests.post(
#                 f"{API_URL}/chat",
#                 json={"messages": st.session_state.messages},
#                 stream=True,
#             )

#             full_text = ""

#             for chunk in response.iter_content(
#                 chunk_size=1024,
#                 decode_unicode=True,
#             ):
#                 if chunk:
#                     full_text += chunk
#                     yield chunk

#             return full_text

#         reply = st.write_stream(response_generator)

#     #
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": reply
#     })
