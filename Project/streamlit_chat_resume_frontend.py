import streamlit as st
from chat_bot_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid


# these are my utility function
def generatr_thread_id():
    thread_id = uuid.uuid4()
    return thread_id


# will create new thread id and that thread id in session
def reset_chat():
    thread_id = generatr_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"] = []


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


# if you want to load thread id histroy from langgraph that's how you can do by useing get_state
def load_converstation(thread_id):
    return chatbot.get_state(config={"configurable": {"thread_id": thread_id}}).values[
        "messages"
    ]


# here i am defining sesstion state data
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generatr_thread_id()


if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

# this will exectute i newlwy enter in my chat bot or can hard refresh my browser because everything went remove from sesstion state
add_thread(st.session_state["thread_id"])


message_history = st.session_state["message_history"]

# define sidebar
st.sidebar.title("LnagGraph Chatbot")
if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()

st.sidebar.header("My Conversations")

for thread_id in st.session_state["chat_threads"][::-1]:  # reverse chat id
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"] = (
            thread_id  # again adding in session current chat_id
        )
        # here i am loding chread chat data from langgraph
        messages = load_converstation(thread_id)

        # so in langgrah data is store in diff way so for handle backward compatiblity we converting into old format
        temp_messages = []
        for message in messages:
            if isinstance(messages, HumanMessage):
                role = "user"
            else:
                role = "assistant"
            temp_messages.append({"role": role, "content": message.content})
        st.session_state["message_history"] = temp_messages
# displaying all chat in chat window for particular thread id
for message in message_history:
    with st.chat_message(message["role"]):
        st.text(message["content"])
# simple taking input
user_input = st.chat_input("Type here")

if user_input:
    message_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}
    # i have define lot of thing about this functinality in streamlit_streaming py file take a look and you will get an idea what is happening
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {"messages": HumanMessage(content=user_input)},
                config=CONFIG,
                stream_mode="messages",
            )
        )
        message_history.append({"role": "assistant", "content": ai_message})
