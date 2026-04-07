from config.settings import Settings

Settings.validate()

import streamlit as st
import json
import os
from services.gemini_service import generate_response
from prompts.career_prompt import build_prompt

CHAT_FILE = "chats.json"

# ----------------------------
# 💾 Load / Save Chats
# ----------------------------
def load_chats():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    return {}

def save_chats():
    with open(CHAT_FILE, "w") as f:
        json.dump(st.session_state.conversations, f)


# ----------------------------
# 🔧 Init Session
# ----------------------------
if "conversations" not in st.session_state:
    st.session_state.conversations = load_chats()

if "current_chat" not in st.session_state:
    if st.session_state.conversations:
        st.session_state.current_chat = list(st.session_state.conversations.keys())[0]
    else:
        st.session_state.current_chat = "Chat 1"
        st.session_state.conversations["Chat 1"] = []

if "rename_chat" not in st.session_state:
    st.session_state.rename_chat = None


# ----------------------------
# 🎨 Page Config
# ----------------------------
st.set_page_config(page_title="AI Career Advisor", layout="wide")


# ----------------------------
# 🎨 Sidebar
# ----------------------------
with st.sidebar:
    st.title("💬 Chats")

    # ➕ New Chat
    if st.button("➕ New Chat"):
        new_chat = f"Chat {len(st.session_state.conversations) + 1}"
        st.session_state.conversations[new_chat] = []
        st.session_state.current_chat = new_chat
        save_chats()
        st.rerun()

    st.markdown("---")

    # 📜 Chat List
    for chat in list(st.session_state.conversations.keys()):
        col1, col2, col3 = st.columns([5, 1, 1])

        # Select Chat
        if col1.button(chat, key=f"select_{chat}"):
            st.session_state.current_chat = chat
            st.rerun()

        # ✏️ Rename
        if col2.button("✏️", key=f"rename_{chat}"):
            st.session_state.rename_chat = chat

        # 🗑️ Delete
        if col3.button("🗑️", key=f"delete_{chat}"):
            del st.session_state.conversations[chat]

            if st.session_state.conversations:
                st.session_state.current_chat = list(st.session_state.conversations.keys())[0]
            else:
                st.session_state.current_chat = "Chat 1"
                st.session_state.conversations["Chat 1"] = []

            save_chats()
            st.rerun()

    # ----------------------------
    # ✏️ Rename Input (FIXED)
    # ----------------------------
    if st.session_state.rename_chat:
        old_name = st.session_state.rename_chat

        st.markdown("### ✏️ Rename Chat")
        new_name = st.text_input("New name:", value=old_name)

        col1, col2 = st.columns(2)

        if col1.button("✅ Save"):
            if new_name and new_name != old_name:
                st.session_state.conversations[new_name] = st.session_state.conversations.pop(old_name)
                st.session_state.current_chat = new_name
                save_chats()

            st.session_state.rename_chat = None
            st.rerun()

        if col2.button("❌ Cancel"):
            st.session_state.rename_chat = None
            st.rerun()


# ----------------------------
# 🎯 Current Chat
# ----------------------------
chat_name = st.session_state.current_chat
chat_history = st.session_state.conversations[chat_name]

st.title(f"🤖 {chat_name}")


# ----------------------------
# 💬 Display Messages
# ----------------------------
for role, content in chat_history:
    with st.chat_message(role):
        st.markdown(content)


# ----------------------------
# ✍️ Input Box
# ----------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    chat_history.append(("user", user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            prompt = build_prompt(user_input, [m[1] for m in chat_history])
            response = generate_response(prompt)
            st.markdown(response)

    # Save response
    chat_history.append(("assistant", response))

    save_chats()
