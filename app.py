import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

st.set_page_config(page_title="Tiger 4 India - Residence Verification", page_icon="📄")

st.title("🏡 Residence Verification Report Generator")
st.write("কেৱল তলৰ খালী ঠাইবোৰ পূৰণ কৰক, বাকী ফৰ্মখন নিজে নিজে এই PDF টোৰ দৰে প্ৰস্তুত হৈ যাব!")

# --- এডিট কৰিবলগীয়া ইনপুটসমূহ (User Editable Fields) ---
st.subheader("📝 প্ৰয়োজনীয় তথ্যসমূহ সলনি কৰক:")

verifier_remark = st.text_area("Verifier Remarks:", "I Visited At The Provided Address & I Met with the Applicant. Neighbor’s feedbacks Satisfactory. There is no Adverse report found as per enquiry. Hence The Residence Report is Positive.")
branch_name = st.text_input("Branch Name:", "SBINMCH BRANCH")
lifting_date = st.text_input("Lifting Date:", "29.09.2026")
applicant_name = st.text_input("Name of Applicant:", "GHUNUCHA DEVI")
residence_address = st.text_area("Residence Address:", "LALIT CHANDRA NATH, VILL PACHIM DIGHALDARI, DIGHALDARI, NAGAON, ASSAM. 782103")
date_of_visit = st.text_input("Date of Visit:", "30.09.2026")
time_of_visit = st.text_input("Time of Visit:", "04:36:00 PM")
person_met = st.text_input("Person Met:", "GHUNUCHA DEVI")
relationship = st.text_input("Relationship:", "WIFE")
total_family_members = st.text_input("Total Family Members:", "05")
total_earning = st.text_input("Total Earnings Members:", "03")
ownership = st.text_input("Ownership:", "OWN HOUSE")
purpose = st.text_input("Purpose:", "SURYA GHAR LOAN")
neighbor_feedback = st.text_input("Neighbor's Feedback:", "GOOD")
remarks_status = st.text_input("Remarks:", "Positive")
verifier_name = st.text_input("Verifier Name:", "IKABAL HUSSAIN")

# ফটো আপলোড কৰাৰ সুবিধা
uploaded_photo = st.file_uploader("ঘৰৰ ফটো বা Selfie আপলোড কৰক (যিটো PDF ৰ তলত থাকিব):", type=["jpg", "jpeg", "png"])

# PDF বনোৱা বটন
if st.button("🚀 PDF ৰিপৰ্ট প্ৰস্তুত কৰক"):
    pdf_filename = "Residence_Verification_Report.pdf"
    
    # PDF Page Setup
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    
    # Header Information (Tiger 4 India Limited)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 30, "TIGER 4 INDIA LIMITED")
    c.setFont("Helvetica", 8)
    c.drawString(50, height - 42, "Corporate Office: #7, Lower Ground Floor, L.S.C., B-1, Vasant Kunj, New Delhi-110070 India")
    c.drawString(50, height - 52, "E-mail id: tigerindialtd@gmail.com | Mobile: 8282864451")
    
    # Report Title
    c.setFont("Helvetica-Bold", 10)
    c.drawString(220, height - 70, "Residence Verification Report")
    
    # Body Details
    c.setFont("Helvetica", 8)
    y = height - 90
    
    details = [
        f"Verifier Remarks: {verifier_remark}",
        f"Branch Name: {branch_name} | Lifting Date: {lifting_date}",
        f"Name of Applicant: {applicant_name}",
        f"Residence Address: {residence_address}",
        f"Date of Visit: {date_of_visit} | Time of Visit: {time_of_visit}",
        f"Person Met: {person_met} | Relationship: {relationship}",
        f"Total Family Members: {total_family_members} | Total Earnings Members: {total_earning}",
        f"Ownership: {ownership} | Purpose: {purpose}",
        f"Neighbor’s Feedback: {neighbor_feedback} | Remarks: {remarks_status}",
        f"Verifier Name: {verifier_name}"
    ]
    
    for line in details:
        c.drawString(50, y, line)
        y -= 15
        
    # যদি ফটো আপলোড কৰে
    if uploaded_photo is not None:
        img_path = "temp_ver_img.jpg"
        with open(img_path, "wb") as f:
            f.write(uploaded_photo.getbuffer())
        try:
            c.drawImage(img_path, 50, y - 180, width=200, height=150)
        except:
            pass
            
    c.save()
    
    st.success("✨ আপোনাৰ PDF ৰিপৰ্ট সফলভাৱে তৈয়াৰ হ'ল!")
    
    # Download Button
    with open(pdf_filename, "rb") as pdf_file:
        st.download_button(
            label="📥 PDF ডাউনলোড কৰক",
            data=pdf_file,
            file_name="Verification_Report.pdf",
            mime="application/pdf"
        )
