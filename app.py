import os
from io import BytesIO
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import base64
import urllib.request

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

HISTORY_FILE = "report_history.json"
GITHUB_TOKEN = "ghp_Vyoe7GNs1kPmgfp5ghg9xAFNtUar72307zYn"
REPO_NAME = "sumonnath252-star/tiger-report"


def load_history():
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{HISTORY_FILE}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            file_content = base64.b64decode(res_data["content"]).decode("utf-8")
            return json.loads(file_content)
    except Exception:
        pass

    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    return json.loads(content)
        except Exception:
            return []
    return []


def save_history(history_list):
    serializable_list = []
    for item in history_list:
        serializable_list.append({
            "Timestamp": item["Timestamp"],
            "Applicant Name": item["Applicant Name"],
            "Branch Name": item["Branch Name"],
            "Customer Mobile": item["Customer Mobile"],
            "FullData": item["FullData"],
        })

    json_data = json.dumps(serializable_list, ensure_ascii=False, indent=4)

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write(json_data)
    except Exception:
        pass

    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{HISTORY_FILE}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
    }

    sha = None
    try:
        req_get = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req_get) as resp:
            sha = json.loads(resp.read().decode())["sha"]
    except Exception:
        pass

    encoded_content = base64.b64encode(json_data.encode("utf-8")).decode("utf-8")
    payload = {
        "message": f"Update report history - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "content": encoded_content,
    }
    if sha:
        payload["sha"] = sha

    try:
        req_put = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="PUT",
        )
        urllib.request.urlopen(req_put)
    except Exception:
        pass


if "report_history" not in st.session_state:
    st.session_state.report_history = load_history()

if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

total_reports = len(st.session_state.report_history)
st.info(f"📊 Muth bonuwa report-or songkha (Total Reports Generated): **{total_reports}**")

st.subheader("⚙️ Quick Status Selection")
col_s1, col_s2 = st.columns(2)
with col_s1:
    solar_install = st.selectbox("Solar Installed?", ["Yes", "No"], key="solar_select")
with col_s2:
    person_met = st.text_input("Person Met *", "OSMAN ALI", key="person_met_quick")

if solar_install == "No":
    auto_verifier_remarks = (
        f"I Visited At The Provided Address & I Met with {person_met} Confirmed His Address. "
        "Neighbor’s feedback Is Satisfactory. There is no Adverse report found as per enquiry. "
        "Hence The Residence Report is Positive."
    )
else:
    auto_verifier_remarks = (
        "I Visited At The Provided Address and found solar panel is successfully installed"
    )

with st.form("verification_form"):
    st.subheader("📋 Applicant & Visit Details (Fields marked with * are mandatory)")
    col1, col2 = st.columns(2)

    with col1:
        branch_name = st.text_input("Branch Name *", "SBI SAMAGURI BRANCH")
        lifting_date = st.text_input("Lifting Date *", "03.10.2026")
        applicant_name = st.text_input("Name of Applicant *", "USUF ALI")
        customer_mobile = st.text_input("Customer Mobile Number *", "9876543210")
        occupation = st.text_input("Occupation", "BUSINESS")
        address = st.text_area(
            "Residence Address *",
            "VILL:LALUNG GAON, P/O-KASORI P/S-JURIA PINCODE-782124 DIST: NAGAON, ASSAM",
        )
        date_of_visit = st.text_input("Date of Visit *", "03.10.2026")
        time_of_visit = st.text_input("Time of Visit *", "09:33:00 AM")
        address_confirmed = st.text_input("Address Confirmed", "YES")
        relationship = st.text_input("Relationship *", "FATHER")
        marital_status = st.text_input("Marital Status", "MARRIED")
        family_members = st.text_input("Total Family Members", "05")
        earning_members = st.text_input("Total Earning Members", "03")
        children = st.text_input("Children", "00")

    with col2:
        is_spouse_working = st.text_input("Is Spouse Working? (Y/N)", "NA")
        spouse_details = st.text_input("If Yes Then Details", "NA")
        ownership = st.text_input("Ownership", "OWN HOUSE")
        years_in_house = st.text_input("No of Years in Existing House", "BY BIRTH")
        locality = st.text_input("Locality", "NA")
        unit = st.text_input("Unit", "GROUND FLOOR")
        construction = st.text_input("Construction", "CEMENTED")
        roof_type = st.text_input("Type of Roof", "CONCRETE")
        approx_area = st.text_area("Approx Area of the House (Sq Ft.)", "1000 SQFT")
        floor = st.text_input("Floor of the House", "GROUND")
        assets_seen = st.text_input("Assets Seen? (Y/N)", "YES")
        vehicle = st.text_input("Vehicle", "NA")
        portrait = st.text_input("Portrait of Political Leaders", "NO")

    st.subheader("📊 Additional Details & Remarks")
    col3, col4 = st.columns(2)
    with col3:
        purpose = st.text_input("Purpose", "SURYA GHAR LOAN")
        prop_location = st.text_input("Proposed Property Location", "EASY")
        loans_taken = st.text_input("Any Loans Taken? (Y/N)", "NO")
        financier = st.text_input("Financier", "NA")
        emi = st.text_input("EMI", "NA")
        accessibility = st.text_input("Accessibility of Office", "Easy")
    with col4:
        neighbor_name = st.text_input("Neighbor Name", "RAHIM UDDIN")
        neighbor_mobile = st.text_input("Neighbor Mobile Number", "9123456789")
        neighbors_feedback = st.text_input("Neighbor's Feedback", "GOOD")
        verifier_remarks = st.text_input("Verifier Remarks", value=auto_verifier_remarks)
        remarks = st.text_input("Remarks", "Positive")
        prev_applied = st.text_input("Did Customer Apply Previously?", "NA")
        prev_date = st.text_input("Date of Previous File", "NA")
        recommendation = st.text_input("Recommendation", "Yes")
        verifier_name = st.text_input("Verifier Name", "EKRAMUL HUSSAIN")

    st.subheader("📸 Upload Verification Photos (Dukhan photo upload korok)")
    uploaded_photo1 = st.file_uploader(
        "Upload House/Location Photo 1", type=["jpg", "jpeg", "png"], key="p1"
    )
    uploaded_photo2 = st.file_uploader(
        "Upload Customer/Verifier Photo 2", type=["jpg", "jpeg", "png"], key="p2"
    )

    st.subheader("🔵 Upload Authorized Seal Image")
    uploaded_seal = st.file_uploader(
        "Upload Seal Image (PNG/JPG)", type=["jpg", "jpeg", "png"], key="seal"
    )

    submitted = st.form_submit_button("Generate Files")


def generate_report_files(data_dict, p1, p2, seal):
    pdf_buffer = BytesIO()
