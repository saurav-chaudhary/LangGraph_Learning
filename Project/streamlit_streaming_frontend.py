import streamlit as st
from chat_bot_backend import chatbot
from langchain_core.messages import HumanMessage

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
message_history = st.session_state["message_history"]


for message in message_history:
    with st.chat_message(message["role"]):
        st.text(message["content"])
user_input = st.chat_input("Type here")


if user_input:
    message_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    # write_stream() requires a generator, and chatbot.stream() returns data
    # incrementally through a generator. With stream_mode="messages", it streams
    # message chunks (tokens or groups of tokens), which write_stream() displays
    # progressively.
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {"messages": HumanMessage(content=user_input)},
                config={"configurable": {"thread_id": "1"}},
                stream_mode="messages",
            )
        )
        message_history.append({"role": "assistant", "content": ai_message})
