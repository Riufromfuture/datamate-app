import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
from io import BytesIO
from paddleocr import PaddleOCR
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the .env file into environment variables
# Navbar
from components.navbar import show_navbar

st.set_page_config(page_title="Chat with PDF", page_icon="📄")
show_navbar()
st.title("📄 Chat with PDF")

# GROQ API key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("❌ GROQ_API_KEY is missing. Please set it in your environment or Streamlit secrets.")
else:
    client = Groq(api_key=groq_api_key)

# 🔄 Cache PaddleOCR reader
@st.cache_resource
def load_ocr_reader():
    return PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

ocr = load_ocr_reader()

# Session state
if "pdf_messages" not in st.session_state:
    st.session_state["pdf_messages"] = [{"role": "assistant", "content": "Ask your questions!"}]
if "pdf_chat_history" not in st.session_state:
    st.session_state["pdf_chat_history"] = []

uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
if uploaded_pdf:
    text_chunks = []

    with fitz.open(stream=uploaded_pdf.read(), filetype="pdf") as doc:
        total_pages = len(doc)
        progress = st.progress(0, text="🔍 Processing PDF...")

        for page_num, page in enumerate(doc):
            text = page.get_text().strip()
            if text:
                if page_num == 0:
                    st.info("Text-based PDF detected ✅")
                text_chunks.append(text)
            else:
                if page_num == 0:
                    st.info("Scanned PDF detected. Running OCR on images 🧠")
                pix = page.get_pixmap(dpi=150)
                img = Image.open(BytesIO(pix.tobytes()))
                ocr_result = ocr.ocr(np.array(img), cls=True)
                ocr_text = " ".join([line[1][0] for block in ocr_result for line in block])
                if ocr_text.strip():
                    text_chunks.append(ocr_text.strip())

            progress.progress((page_num + 1) / total_pages, text=f"Processing page {page_num + 1} of {total_pages}")

    if not text_chunks:
        st.warning("❌ Could not extract any text from the PDF.")
    else:
        pdf_text = "\n\n".join(text_chunks)

        for msg in st.session_state["pdf_messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_query = st.chat_input("Ask a question about this PDF...")

        if user_query:
            st.session_state["pdf_messages"].append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    prompt = f"""
You are a helpful assistant. A user uploaded a PDF document. Based on the following extracted content, answer their question in plain English.

PDF content:
{pdf_text}

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
                        st.session_state["pdf_messages"].append({"role": "assistant", "content": answer})
                        st.session_state["pdf_chat_history"].append({"Q": user_query, "A": answer})
                    except Exception as e:
                        error_msg = f"❌ Error: {e}"
                        st.error(error_msg)
                        st.session_state["pdf_messages"].append({"role": "assistant", "content": error_msg})

        if st.sidebar.button("🗑️ Clear Chat History"):
            st.session_state["pdf_messages"] = [{"role": "assistant", "content": "Ask your questions!"}]
            st.session_state["pdf_chat_history"] = []
            st.rerun()

        if st.session_state["pdf_chat_history"]:
            if st.sidebar.download_button("📥 Download Chat",
                data=pd.DataFrame(st.session_state["pdf_chat_history"]).to_csv(index=False),
                file_name="pdf_chat_history.csv",
                mime="text/csv"):
                st.sidebar.success("Downloaded!")
else:
    st.info("Please upload a PDF to begin.")
