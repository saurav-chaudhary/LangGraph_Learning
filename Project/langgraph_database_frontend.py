import streamlit as st
from langgraph_database_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid


# these are my utility functions
def generatr_thread_id():
    thread_id = str(uuid.uuid4())
    return thread_id


# will create new thread id and store that thread id in session
def reset_chat():
    thread_id = generatr_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"] = []


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


# if you want to load thread id history from LangGraph,
# that's how you can do it by using get_state
def load_converstation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})

    return state.values.get("messages", [])


# here I am defining session state data
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generatr_thread_id()


if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()


# this will execute if I newly enter in my chatbot
# or can hard refresh my browser because everything went from session state
add_thread(st.session_state["thread_id"])


# define sidebar
st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()


st.sidebar.header("My Conversations")


for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id)):
        # again adding in session current chat_id
        st.session_state["thread_id"] = thread_id

        # here I am loading thread chat data from LangGraph
        messages = load_converstation(thread_id)

        # so in LangGraph data is stored in a different way,
        # for handling backward compatibility we convert it into old format
        temp_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = "user"
            else:
                role = "assistant"

            temp_messages.append({"role": role, "content": message.content})

        st.session_state["message_history"] = temp_messages

        # reload Streamlit so selected conversation is displayed
        st.rerun()


# displaying all chat in chat window for particular thread id
message_history = st.session_state["message_history"]

for message in message_history:
    with st.chat_message(message["role"]):
        st.text(message["content"])


# simple taking input
user_input = st.chat_input("Type here")


if user_input:
    message_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.text(user_input)

    # current thread configuration
    CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}

    # I have defined a lot of things about this functionality
    # in streamlit_streaming.py file.
    # Take a look there and you will get an idea of what is happening here.
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            )
        )

        message_history.append({"role": "assistant", "content": ai_message})
