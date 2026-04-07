import streamlit as st

def init_memory():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def add_to_memory(user, bot):
    st.session_state.chat_history.append(f"User: {user}")
    st.session_state.chat_history.append(f"Bot: {bot}")

def get_memory():
    return st.session_state.chat_history