 
import streamlit as st

def show_sidebar():
    # Inject CSS to style sidebar links
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] a {
                font-weight: bold;
                text-transform: capitalize;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar content
    st.sidebar.title("🔍 Navigation")
    st.sidebar.page_link("app.py", label="🏠 App")
    st.sidebar.page_link("pages/chat_mysql.py", label="💬 MySQL Chat")
    st.sidebar.page_link("pages/chat_excel.py", label="💬 Excel Chat")
    st.sidebar.page_link("pages/history.py", label="📜 Chat History")
    st.sidebar.page_link("pages/login.py", label="🔐 Login / Register")

# show_sidebar()
