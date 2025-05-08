 
import streamlit as st

def show_navbar():
    st.markdown(
        """
        <style>
            .navbar {
                background: linear-gradient(135deg, #006d77, #00b4a8); /* Slightly lighter blue-green */
                padding: 1.5rem;
                border-radius: 10px;
                margin-bottom: 2rem;
                font-size: 18px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
                color: #ffffff;
            }
            .navbar h1 {
                font-size: 2.2em;
                margin-bottom: 0.2rem;
                color: #ffffff;
            }
            .navbar p {
                font-size: 1.1em;
                color: #e0f7f4;
                margin: 0;
            }
        </style>
        <div class="navbar">
            <h1>Welcome to <strong>DataMate</strong>
            <img src="https://img.icons8.com/?size=100&id=112370&format=png&color=000000" alt="icon" width="28" height="28" style="margin-left: 8px; vertical-align: middle;">
            </h1>
            <p>Your AI-powered assistant for interacting with the data</p>
        </div>
        """,
        unsafe_allow_html=True
    )
