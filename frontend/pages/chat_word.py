import streamlit as st
import pandas as pd
from docx import Document
from groq import Groq
from dotenv import load_dotenv
import os
from components.navbar import show_navbar

load_dotenv()  # This loads the .env file into environment variables

st.set_page_config(page_title="Chat with Word Document", page_icon="📄")
show_navbar()
st.title("📄 Chat with Word Document")

# Initialize Groq
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("❌ GROQ_API_KEY is missing. Please set the environment variable.")
else:
    client = Groq(api_key=groq_api_key)

# Initialize chat state
if "word_messages" not in st.session_state:
    st.session_state["word_messages"] = [{"role": "assistant", "content": "Ask your questions!"}]
if "word_chat_history" not in st.session_state:
    st.session_state["word_chat_history"] = []

uploaded_word = st.file_uploader("Upload a Word document", type=["docx"])
if uploaded_word:
    text_chunks = []

    # Extract text using python-docx
    doc = Document(uploaded_word)
    for para in doc.paragraphs:
        if para.text.strip():
            text_chunks.append(para.text.strip())

    # Combine content
    word_text = "\n\n".join(text_chunks[:])  # Limit for token efficiency

    # Show conversation history
    for msg in st.session_state["word_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask a question about this Word document...")

    if user_query:
        st.session_state["word_messages"].append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                prompt = f"""
You are a helpful assistant. A user uploaded a Word document. Based on the following extracted content, answer their question in plain English.

Word document content:
{word_text}

User's question: {user_query}

Answer:"""
                try:
                    response = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.4
                    )
                    answer = response.choices[0].message.content.strip()
                    st.markdown("**Answer:**")
                    st.write(answer)
                    st.session_state["word_messages"].append({"role": "assistant", "content": answer})
                    st.session_state["word_chat_history"].append({"Q": user_query, "A": answer})
                except Exception as e:
                    error_msg = f"❌ Error: {e}"
                    st.error(error_msg)
                    st.session_state["word_messages"].append({"role": "assistant", "content": error_msg})

    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state["word_messages"] = [{"role": "assistant", "content": "Ask your questions!"}]
        st.session_state["word_chat_history"] = []
        st.rerun()

    if st.session_state["word_chat_history"]:
        if st.sidebar.download_button("📥 Download Chat",
            data=pd.DataFrame(st.session_state["word_chat_history"]).to_csv(index=False),
            file_name="word_chat_history.csv",
            mime="text/csv"):
            st.sidebar.success("Downloaded!")
else:
    st.info("Please upload a Word document to begin.")
