@echo off 
start cmd /k "uvicorn backend.main:app --reload" 
timeout /t 5 
start cmd /k "streamlit run frontend/app.py" 
