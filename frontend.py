import streamlit as st
import requests

st.set_page_config(page_title="Personal Chatbot", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .chat-container {
        max-width: 600px;
        margin: auto;
    }
    .user-bubble {
        background-color: #DCF8C6;
        color: #222;
        padding: 10px 16px;
        border-radius: 18px 18px 2px 18px;
        margin-bottom: 8px;
        margin-left: 60px;
        text-align: left;
        display: inline-block;
    }
    .bot-bubble {
        background-color: #F1F0F0;
        color: #222;
        padding: 10px 16px;
        border-radius: 18px 18px 18px 2px;
        margin-bottom: 8px;
        margin-right: 60px;
        text-align: left;
        display: inline-block;
    }
    .avatar {
        width: 32px;
        height: 32px;
        display: inline-block;
        vertical-align: top;
        margin-right: 8px;
    }
    .chat-row {
        display: flex;
        align-items: flex-start;
        margin-bottom: 2px;
    }
    .user-row {
        flex-direction: row-reverse;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; font-size:2rem; font-weight:bold; margin-bottom: 1rem;'>🤖 Personal Chatbot</div>
""", unsafe_allow_html=True)

backend_url = "http://localhost:8000/chat"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat message display
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for role, msg in st.session_state["messages"]:
    if role == "user":
        st.markdown(f"""
        <div class='chat-row user-row'>
            <div class='avatar'>🧑</div>
            <div class='user-bubble'>{msg}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='chat-row'>
            <div class='avatar'>🤖</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<div class='bot-bubble'>{msg}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Input area
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("Your message:", "", key="input", height=60)
    submitted = st.form_submit_button("Send", use_container_width=True)

if submitted and user_input.strip():
    st.session_state["messages"].append(("user", user_input.strip()))
    with st.spinner("Chatbot is thinking..."):
        try:
            response = requests.post(backend_url, json={"message": user_input.strip()}, timeout=30)
            if response.status_code == 200:
                bot_reply = response.json()["response"]
            else:
                error_msg = response.json().get('error', 'Unknown error')
                bot_reply = f"**Error:** {error_msg}"
        except Exception as e:
            bot_reply = f"**Error:** Backend unavailable or network error.\n{e}"
        st.session_state["messages"].append(("bot", bot_reply))
    st.rerun()  # To auto-scroll and clear input 