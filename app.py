import os
from io import BytesIO
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from docx import Document

st.set_page_config(page_title="Residence Verification Report Generator", layout="centered")

st.title("🏡 Residence Verification Report Generator")
st.write("ফৰ্মৰ তথ্যসমূহ পৰিৱৰ্তন কৰি PDF আৰু Word দুয়োটাই ডাউনলোড কৰক:")

# ইনপুট ফৰ্ম (সকলো এডিট কৰিব পৰা হ'ব)
with st.form("verification_form"):
    st.subheader("📋 Applicant & Visit Details (Edit as needed)")
    col1, col2 = st.columns(2)
    
    with col1:
        applicant_name = st.text_input("Name of Applicant", "GHUNUCHA DEVI")
        branch_name = st.text_input("Branch Name", "SBINMCH BRANCH")
        lifting_date = st.text_input("Lifting Date", "29.09.2026")
        date_of_visit = st.text_input("Date of Visit", "30.09.2026")
        time_of_visit = st.text_input("Time of Visit", "04:36:00 PM")
        address = st.text_area("Residence Address", "LALIT CHANDRA NATH, VILL PACHIM DIGHALDARI, DIGHALDARI, NAGAON, ASSAM. 782103")
        
    with col2:
        verifier_name = st.text_input("Verifier Name", "IKABAL HUSSAIN")
        person_met = st.text_input("Person Met", "GHUNUCHA DEVI")
        relationship = st.text_input("Relationship", "WIFE")
        family_members = st.text_input("Total Family Members", "05")
        earning_members = st.text_input("Total Earning Members", "03")
        ownership = st.text_input("Ownership", "OWN HOUSE")
        construction = st.text_input("Construction & Roof", "CEMENTED / CONCRETE")

    st.subheader("📸 Upload Verification Photos (দুখন ফটো আপলোড কৰক)")
    uploaded_photo1 = st.file_uploader("Upload House/Location Photo 1", type=["jpg", "jpeg", "png"], key="p1")
    uploaded_photo2 = st.file_uploader("Upload Customer/Verifier Photo 2", type=["jpg", "jpeg", "png"], key="p2")

    submitted = st.form_submit_button("Generate Files")

if submitted:
    # --- PDF Generation ---
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#003366'),
        alignment=1,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'SubTitleStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#555555'),
        alignment=1,
        spaceAfter=15
    )
    
    story.append(Paragraph("<b>TIGER 4 INDIA LIMITED</b>", title_style))
    story.append(Paragraph("Corporate Office: #7, Lower Ground Floor, L.S.C., B-1, Vasant Kunj, New Delhi-110070<br/>E-mail: tigindialtd@gmail.com | Mobile: 8282864451", subtitle_style))
    story.append(Paragraph("<b><u>RESIDENCE VERIFICATION REPORT</u></b>", ParagraphStyle('H2', parent=title_style, fontSize=13, textColor=colors.HexColor('#222222'))))
    story.append(Spacer(1, 10))
    
    data = [
        [Paragraph("<b>Branch Name:</b>", styles['Normal']), Paragraph(branch_name, styles['Normal']), Paragraph("<b>Lifting Date:</b>", styles['Normal']), Paragraph(lifting_date, styles['Normal'])],
        [Paragraph("<b>Applicant Name:</b>", styles['Normal']), Paragraph(applicant_name, styles['Normal']), Paragraph("<b>Date of Visit:</b>", styles['Normal']), Paragraph(date_of_visit)],
        [Paragraph("<b>Address:</b>", styles['Normal']), Paragraph(address, styles['Normal']), Paragraph("<b>Time of Visit:</b>", styles['Normal']), Paragraph(time_of_visit)],
        [Paragraph("<b>Person Met:</b>", styles['Normal']), Paragraph(person_met, styles['Normal']), Paragraph("<b>Relationship:</b>", styles['Normal']), Paragraph(relationship)],
        [Paragraph("<b>Family / Earning:</b>", styles['Normal']), Paragraph(f"Family: {family_members} | Earning: {earning_members}", styles['Normal']), Paragraph("<b>Ownership:</b>", styles['Normal']), Paragraph(ownership)],
        [Paragraph("<b>Construction:</b>", styles['Normal']), Paragraph(construction, styles['Normal']), Paragraph("<b>Purpose:</b>", styles['Normal']), Paragraph("SURYA GHAR LOAN", styles['Normal'])],
        [Paragraph("<b>Verifier Name:</b>", styles['Normal']), Paragraph(verifier_name, styles['Normal']), Paragraph("<b>Final Status:</b>", styles['Normal']), Paragraph("<b><font color='green'>POSITIVE</font></b>", styles['Normal'])],
    ]
    
    t = Table(data, colWidths=[110, 160, 90, 180])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F9F9F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CCCCCC')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DDDDDD')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Verification Photos:</b>", styles['Heading2']))
    story.append(Spacer(1, 5))
    
    img_data = []
    temp_files = []
    
    for idx, up_file in enumerate([uploaded_photo1, uploaded_photo2]):
        if up_file is not None:
            temp_path = f"temp_img_{idx}.jpg"
            with open(temp_path, "wb") as f:
                f.write(up_file.getbuffer())
            temp_files.append(temp_path)
            img_data.append(RLImage(temp_path, width=220, height=160))
            
    if len(img_data) > 0:
        while len(img_data) < 2:
            img_data.append("")
        photo_table = Table([[img_data[0], img_data[1]]], colWidths=[270, 270])
        photo_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(photo_table)

    story.append(Spacer(1, 20))
    
    # চহী আৰু চীলৰ অংশ (Authorized Signature with Seal)
    sig_data = [
        [Paragraph("<b>Neighbor’s Feedback:</b> Good", styles['Normal']), Paragraph(f"<b>Verifier Name:</b> {verifier_name}<br/><br/><b>Authorized Signature with Seal</b>", styles['Normal'])]
    ]
    sig_table = Table(sig_data, colWidths=[270, 270])
    story.append(sig_table)

    doc.build(story)
    pdf_buffer.seek(0)
    
    # --- Word (.docx) Generation ---
    doc_word = Document()
    doc_word.add_heading("TIGER 4 INDIA LIMITED", level=1)
    doc_word.add_paragraph("Corporate Office: #7, Lower Ground Floor, L.S.C., B-1, Vasant Kunj, New Delhi-110070\nE-mail: tigindialtd@gmail.com | Mobile: 8282864451")
    doc_word.add_heading("RESIDENCE VERIFICATION REPORT", level=2)
    
    doc_word.add_paragraph(f"Branch Name: {branch_name} | Lifting Date: {lifting_date}")
    doc_word.add_paragraph(f"Name of Applicant: {applicant_name}")
    doc_word.add_paragraph(f"Residence Address: {address}")
    doc_word.add_paragraph(f"Date of Visit: {date_of_visit} | Time: {time_of_visit}")
    doc_word.add_paragraph(f"Person Met: {person_met} | Relationship: {relationship}")
    doc_word.add_paragraph(f"Total Family Members: {family_members} | Earning Members: {earning_members}")
    doc_word.add_paragraph(f"Ownership: {ownership} | Construction: {construction}")
    doc_word.add_paragraph(f"Verifier Name: {verifier_name}")
    doc_word.add_paragraph("Remarks: Positive")
    doc_word.add_paragraph("\nAuthorized Signature with Seal")
    
    word_buffer = BytesIO()
    doc_word.save(word_buffer)
    word_buffer.seek(0)
    
    for tf in temp_files:
        if os.path.exists(tf):
            os.remove(tf)
            
    st.success("✨ Files successfully generated!")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            label="📥 Download PDF",
            data=pdf_buffer,
            file_name="Residence_Verification_Report.pdf",
            mime="application/pdf"
        )
    with col_d2:
        st.download_button(
            label="📥 Download Word",
            data=word_buffer,
            file_name="Residence_Verification_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
