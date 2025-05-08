import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
from io import BytesIO
from groq import Groq
from dotenv import load_dotenv
import os

# Google Cloud Vision setup
from google.cloud import vision
from google.oauth2 import service_account

# Navbar
from components.navbar import show_navbar
load_dotenv()  # This loads the .env file into environment variables
st.set_page_config(page_title="DataMate • Chat PDF", page_icon="https://img.icons8.com/?size=100&id=112370&format=png&color=000000")
show_navbar()

# Title 
st.markdown(
    """
    <div style='display: flex; align-items: center; gap: 20px; margin-bottom: 1rem;'>
        <img src='https://img.icons8.com/?size=100&id=299&format=png&color=000000' width='50' height='50' style='margin-left: 10px;'/>
        <h1 style='margin: 0;'>Chat with PDF</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Setup Google Vision client
try:
    creds = service_account.Credentials.from_service_account_info({
        "type": st.secrets["GCP_TYPE"],
        "project_id": st.secrets["GCP_PROJECT_ID"],
        "private_key_id": st.secrets["GCP_PRIVATE_KEY_ID"],
        "private_key": st.secrets["GCP_PRIVATE_KEY"],
        "client_email": st.secrets["GCP_CLIENT_EMAIL"],
        "client_id": st.secrets["GCP_CLIENT_ID"],
        "auth_uri": st.secrets["GCP_AUTH_URI"],
        "token_uri": st.secrets["GCP_TOKEN_URI"],
        "auth_provider_x509_cert_url": st.secrets["GCP_AUTH_PROVIDER_CERT_URL"],
        "client_x509_cert_url": st.secrets["GCP_CLIENT_CERT_URL"],
        "universe_domain": st.secrets["GCP_UNIVERSE_DOMAIN"]
    })
    vision_client = vision.ImageAnnotatorClient(credentials=creds)
except Exception as e:
    st.error(f"❌ Failed to initialize Google Vision client: {str(e)}")
    st.stop()

# GROQ API key
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except KeyError:
    st.error("❌ GROQ_API_KEY is missing from Streamlit secrets. Please add it to your `.streamlit/secrets.toml`.")
    st.stop()
    
# Session state
if "pdf_messages" not in st.session_state:
    st.session_state["pdf_messages"] = [{"role": "assistant", "content": "Ask your questions!"}]
if "pdf_chat_history" not in st.session_state:
    st.session_state["pdf_chat_history"] = []

# File uploader
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
                    st.info("Scanned PDF detected. Running Google OCR 🧠")
                pix = page.get_pixmap(dpi=150)
                img = Image.open(BytesIO(pix.tobytes()))

                # Convert image to byte array for Google Vision API
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format="PNG")
                image = vision.Image(content=img_byte_arr.getvalue())

                response = vision_client.document_text_detection(image=image)
                ocr_text = response.full_text_annotation.text.strip()

                if ocr_text:
                    text_chunks.append(ocr_text)

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
                        error_str = str(e)
                        if "Request too large" in error_str or "'code': 'rate_limit_exceeded'" in error_str:
                            error_msg = "❌ File too long. The document exceeds the model's processing limit. Please upload a shorter PDF or split it into smaller parts."
                        else:
                            error_msg = f"❌ Error: {e}"
                        st.error(error_msg)
                        st.session_state["pdf_messages"].append({"role": "assistant", "content": error_msg})

        # Clear chat history
        if st.sidebar.button("🗑️ Clear Chat History"):
            st.session_state["pdf_messages"] = [{"role": "assistant", "content": "Ask your questions!"}]
            st.session_state["pdf_chat_history"] = []
            st.rerun()

        # Chat download option
        if st.session_state["pdf_chat_history"]:
            if st.sidebar.download_button("📥 Download Chat",
                data=pd.DataFrame(st.session_state["pdf_chat_history"]).to_csv(index=False),
                file_name="pdf_chat_history.csv",
                mime="text/csv"):
                st.sidebar.success("Downloaded!")
else:
    st.info("Please upload a PDF to begin.")
