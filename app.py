"""Simple chat UI. Run: streamlit run app.py"""
import streamlit as st
from chatbot import FAQBot

st.set_page_config(page_title="FAQ Chatbot", page_icon="💬")
st.title("💬 FAQ Chatbot")

@st.cache_resource
def load_bot():
    return FAQBot()

bot = load_bot()
if "history" not in st.session_state:
    st.session_state.history = [("assistant", "Hi! Ask me anything about orders, shipping, returns or payments.")]

for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)

if q := st.chat_input("Type your question..."):
    st.session_state.history.append(("user", q))
    st.chat_message("user").write(q)
    answer, matched, score = bot.ask(q)
    if matched:
        answer += f"\n\n*Matched FAQ: “{matched}” (similarity {score:.2f})*"
    st.session_state.history.append(("assistant", answer))
    st.chat_message("assistant").write(answer)