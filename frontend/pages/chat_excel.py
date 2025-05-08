import streamlit as st
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
from components.navbar import show_navbar

load_dotenv()  # This loads the .env file into environment variables
# --- Navbar ---
st.set_page_config(page_title="Excel Chat", page_icon="https://img.icons8.com/?size=100&id=11566&format=png&color=000000")
show_navbar()

st.markdown(
    """
    <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 1rem;'>
        <img src='https://img.icons8.com/?size=100&id=11566&format=png&color=000000' width='40' height='40'/>
        <h1 style='margin: 0;'>Chat with Excel Sheet</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize Groq
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("❌ GROQ_API_KEY is missing. Please set the environment variable.")
else:
    client = Groq(api_key=groq_api_key)

# Initialize chat state
if "excel_messages" not in st.session_state:
    st.session_state["excel_messages"] = [{"role": "assistant", "content": "Ask your questions!"}]
if "excel_cleaned_history" not in st.session_state:
    st.session_state["excel_cleaned_history"] = []

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    total_pages = len(sheet_names)
    progress = st.progress(0, text="Starting sheet processing...")

    all_dfs = []
    for page_num, sheet in enumerate(sheet_names):
        df = pd.read_excel(xls, sheet_name=sheet)
        df['__sheet_name__'] = sheet  # Track sheet origin if needed
        all_dfs.append(df)

        progress.progress((page_num + 1) / total_pages, text=f"Loaded sheet {page_num + 1} of {total_pages}")

    # Show chat history
    for msg in st.session_state["excel_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask a question about your data...")

    if user_query:
        st.session_state["excel_messages"].append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                clean_df = df.copy()
                clean_df.dropna(how='all', inplace=True)

                # Strip column names only if any contain spaces
                if clean_df.columns.str.contains(" ").any():
                    clean_df.columns = clean_df.columns.str.strip()

                # Strip whitespace in string cells only if necessary
                for col in clean_df.select_dtypes(include=['object', 'string']).columns:
                    if clean_df[col].str.contains(r'^\s|\s$', na=False).any():
                        clean_df[col] = clean_df[col].map(lambda x: x.strip() if isinstance(x, str) else x)

                sample_data = clean_df.to_csv(index=False)

                prompt = f"""
You are a data analyst. A user uploaded an Excel file. Based on the following column names and sample data, answer their question in plain English.

Column names: {list(clean_df.columns)}

Sample data:
{sample_data}

User's question: {user_query}

Answer:"""

                try:
                    chat_response = client.chat.completions.create(
                        model="llama3-8b-8192",  # Verify the correct model name
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.4,
                    )
                    response_text = chat_response.choices[0].message.content.strip()
                    st.markdown("**Answer:**")
                    st.write(response_text)

                    # Save assistant reply
                    st.session_state["excel_messages"].append({"role": "assistant", "content": response_text})
                    st.session_state["excel_cleaned_history"].append({"Q": user_query, "A": response_text})

                except Exception as e:
                    error_msg = f"❌ Error generating answer: {e}"
                    st.error(error_msg)
                    st.session_state["excel_messages"].append({"role": "assistant", "content": error_msg})

    # Clear chat history
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state["excel_messages"] = [{"role": "assistant", "content": "Ask your questions!"}]
        st.session_state["excel_cleaned_history"] = []
        st.rerun()

    # Chat download option
    if st.session_state["excel_cleaned_history"]:
        if st.sidebar.download_button("📥 Download Chat", 
            data=pd.DataFrame(st.session_state["excel_cleaned_history"]).to_csv(index=False),
            file_name="excel_chat_history.csv",
            mime="text/csv"):
            st.sidebar.success("Downloaded chat history!")
else:
    st.info("Please upload an Excel file to begin.")
