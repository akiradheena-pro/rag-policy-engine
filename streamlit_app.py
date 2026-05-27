import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="HR Policy Assistant",
    page_icon="🤖",
    layout="centered"
)
st.title("🤖 HR Policy Assistant")
st.markdown("Ask questions about company policies. Answers are grounded in official documents with citations.")

@st.cache_resource
def load_pipeline():
    from app.pipeline import ask_question
    return ask_question

ask_question = load_pipeline()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "sources" in message and message["sources"]:
            st.caption(f"📚 Sources: {', '.join(message['sources'])}")

if prompt := st.chat_input("Ask a question about company policies..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if not os.getenv("GROQ_API_KEY"):
                    st.error("⚠️ GROQ_API_KEY not found in environment variables.")
                    st.stop()

                result = ask_question(prompt)
                answer = result["answer"]
                sources = result["sources"]

                st.write(answer)
                if sources:
                    st.caption(f"📚 Sources: {', '.join(sources)}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
