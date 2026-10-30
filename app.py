import os
from io import BytesIO
import streamlit as st
import pandas as pd
from datetime import datetime
import random
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# CSS code to hide Streamlit branding
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from docx import Document

st.set_page_config(page_title="Residence Verification Report Generator", layout="centered")

st.title("🏡 Residence Verification Report Generator")

# ----------------- LOCAL JSON STORAGE FOR PERMANENT HISTORY -----------------
HISTORY_FILE = "report_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    return json.loads(content)
        except Exception as e:
            return []
    else:
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
        except:
            pass
    return []

def save_history(history_list):
    serializable_list = []
    for item in history_list:
        serializable_list.append({
            "Timestamp": item["Timestamp"],
            "Applicant Name": item["Applicant Name"],
            "Branch Name": item["Branch Name"],
            "Customer Mobile": item["Customer Mobile"],
            "FullData": item["FullData"]
        })
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(serializable_list, f, ensure_ascii=False, indent=4)
    except Exception as e:
        pass

if 'report_history' not in st.session_state:
    st.session_state.report_history = load_history()

if 'email_otp_sent' not in st.session_state:
    st.session_state.email_otp_sent = False

if 'generated_email_otp' not in st.session_state:
    st.session_state.generated_email_otp = ""

if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

# ----------------- EMAIL OTP SENDING FUNCTION -----------------
def send_email_otp(receiver_email, otp_code):
    sender_email = "YOUR_GMAIL@gmail.com"  # <--- আপোনাৰ পঠোৱা জিমেইল একাউণ্ট
    sender_password = "YOUR_APP_PASSWORD"  # <--- জিমেইলৰ App Password
    
    if sender_email == "YOUR_GMAIL@gmail.com":
        return False, "Gmail configuration missing."

    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "🔐 Tiger 4 India - Owner Dashboard Login OTP"
        
        email_body = f"Your secure OTP for Owner Dashboard login is: {otp_code}\n\nDo not share this OTP with anyone."
        message.attach(MIMEText(email_body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
