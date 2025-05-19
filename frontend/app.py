import streamlit as st

st.set_page_config(page_title="DataMate", page_icon="https://img.icons8.com/?size=100&id=112370&format=png&color=000000", layout="wide")

from components.navbar import show_navbar
#from components.sidebar import show_sidebar

# Sidebar & Navbar
# show_sidebar()
show_navbar()

#Option b/w excel and mysql
st.title("💬 Chat with your Data")

# ---------------------------------------------------------------------------------------------------------------------------------------------------#

# --- Custom CSS ---
light_bg = """
    
"""
sidebar_style = """
    
"""

st.markdown(f"""
    <style>
        .stApp {{
            {light_bg}
            background-attachment: fixed;
        }}

        .glass-card {{
            background: rgba(255, 255, 255, 0.25);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            color: #000;
        }}

        .glass-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }}

        .glass-card ul {{
            padding-left: 1.5rem;
            list-style-type: disc;
        }}

        /* Sticky navbar */
        .navbar {{
            position: sticky;
            top: 0;
            z-index: 999;
        }}

        /* Sidebar animation + background */
        section[data-testid="stSidebar"] > div:first-child {{
            transition: all 0.3s ease-in-out;
            {sidebar_style}
        }}
        section[data-testid="stSidebar"]:hover > div:first-child {{
            transform: scale(1.03);
            box-shadow: 0 0 15px rgba(0, 191, 255, 0.3);
        }}

        .cta-button {{
            text-align: center;
            margin-top: 1rem;
        }}
    </style>
""", unsafe_allow_html=True)

# ----------------- CONTENT ------------------ #

st.markdown("""
<div class="glass-card">
    <div class="glass-title">💡 What Can You Do?</div>
    <p></p>
    <ul>
        <li>📊 Explore Excel sheets with Excel Chat</li>
        <li>📄 Understand PDFs, including scanned ones, using PDF Chat</li>
        <li>📝 Ask questions about Word docs with Word Chat</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown('''
<div class="glass-card">
    <div class="glass-title">⚙️ How It Works</div>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div style="text-align: center; flex: 1; min-width: 200px;">
            <img src="https://cdn-icons-png.flaticon.com/512/3523/3523885.png" width="80"/>
            <p><strong>1. Upload </strong></p>
            <p style="font-size: 0.9rem;">Load your file or database.</p>
        </div>
        <div style="text-align: center; flex: 1; min-width: 200px;">
            <img src="https://cdn-icons-png.flaticon.com/512/3649/3649463.png" width="80"/>
            <p><strong>2. Ask Anything</strong></p>
            <p style="font-size: 0.9rem;">Type questions like “Summarize page 1”</br>
            or “Top 5 customers by revenue”.</p>
        </div>
        <div style="text-align: center; flex: 1; min-width: 200px;">
            <img src="https://cdn-icons-png.flaticon.com/512/4149/4149650.png" width="80"/>
            <p><strong>3. Get Instant Answers</strong></p>
            <p style="font-size: 0.9rem;">Powered by Groq’s blazing-fast LLMs,</br>
            results are fast, accurate, and clear.</p>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div class="glass-card">
    <div class="glass-title">✨ Why DataMate?</div>
    <ul>
        <li>🧠 <strong>LLM-powered intelligence</strong></li>
        <li>🖱️ <strong>Easy-to-use interface</strong></li>
        <li>🔐 <strong>Works locally — your data stays with you</strong></li>
        <li>📥 <strong>Download chat history anytime</strong></li>
    </ul>
</div>
''', unsafe_allow_html=True)

# st.markdown('''
# <div class="glass-card">
#     <div class="glass-title">🔑 How to Get Your Own Groq API Key</div>
#     <p>To power natural language processing, SQLMate uses the Groq API with LLMs. You’ll need your own API key to start querying.</p>
#     <ul>
#         <li>Visit <a href="https://console.groq.com/keys" target="_blank">Groq Console</a>.</li>
#         <li>Log in or create an account.</li>
#         <li>Navigate to the <strong>API Keys</strong> section.</li>
#         <li>Click on <strong>Create API Key</strong> and copy it.</li>
#         <li>Paste the key when prompted in the Chat interface.</li>
#     </ul>
#     <p style="font-size: 0.9rem;"><em>Your API key stays only in your current session for privacy and security.</em></p>
# </div>
# ''', unsafe_allow_html=True)

# st.markdown('''
#     <div class="glass-card" style="text-align: center;">
#         <h3>🚀 Ready to try it out?</h3>
#     </div>
# ''', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Made using Streamlit, FastAPI, and LangChain.")






