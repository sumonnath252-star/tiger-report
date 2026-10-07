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
st.write("ফৰ্মৰ তথ্যসমূহ পূৰণ কৰি PDF আৰু Word দুয়োটাই ডাউনলোড কৰক:")

with st.form("verification_form"):
    st.subheader("📋 Applicant & Visit Details")
    col1, col2 = st.columns(2)
    
    with col1:
        branch_name = st.text_input("Branch Name", "SBI SAMAGURI BRANCH")
        lifting_date = st.text_input("Lifting Date", "03.10.2026")
        applicant_name = st.text_input("Name of Applicant", "USUF ALI")
        address = st.text_area("Residence Address", "VILL:LALUNG GAON, P/O-KASORI P/S-JURIA PINCODE-782124 DIST: NAGAON, ASSAM")
        date_of_visit = st.text_input("Date of Visit", "03.10.2026")
        time_of_visit = st.text_input("Time of Visit", "09:33:00 AM")
        address_confirmed = st.text_input("Address Confirmed", "YES")
        person_met = st.text_input("Person Met", "OSMAN ALI")
        relationship = st.text_input("Relationship", "FATHER")
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
        approx_area = st.text_input("Approx Area of the House (Sq Ft.)", "1000 SQFT")
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
        neighbors_feedback = st.text_input("Neighbor's Feedback", "GOOD")
        verifier_remarks = st.text_input("Verifier Remarks", "I Visited At The Provided Address and found solar panel is successfully installed")
        remarks = st.text_input("Remarks", "Positive")
        prev_applied = st.text_input("Did Customer Apply Previously?", "NA")
        prev_date = st.text_input("Date of Previous File", "NA")
        recommendation = st.text_input("Recommendation", "Yes")
        verifier_name = st.text_input("Verifier Name", "EKRAMUL HUSSAIN")

    st.subheader("📸 Upload Verification Photos (দুখন ফটো আপলোড কৰক)")
    uploaded_photo1 = st.file_uploader("Upload House/Location Photo 1", type=["jpg", "jpeg", "png"], key="p1")
    uploaded_photo2 = st.file_uploader("Upload Customer/Verifier Photo 2", type=["jpg", "jpeg", "png"], key="p2")

    # አማক চীল (Seal) আপলোড কৰাৰ অপচন দিয়া হৈছে যাতে হুবহু ফটোখনৰ দৰে চীলটো বহুৱাব পৰা যায়
    st.subheader("🔵 Upload Authorized Seal Image (ঐচ্ছিক)")
    uploaded_seal = st.file_uploader("Upload Seal Image (PNG/JPG)", type=["jpg", "jpeg", "png"], key="seal")

    submitted = st.form_submit_button("Generate Files")

if submitted:
    # --- PDF Generation ---
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=25, leftMargin=25, topMargin=25, bottomMargin=25)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=14, textColor=colors.HexColor('#003366'), alignment=1, spaceAfter=4)
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#555555'), alignment=1, spaceAfter=10)
    
    story.append(Paragraph("<b>TIGER 4 INDIA LIMITED</b>", title_style))
    story.append(Paragraph("Corporate Office: #7, Lower Ground Floor, L.S.C., B-1, Vasant Kunj, New Delhi-110070 India<br/>E-mail id: tigindialtd@gmail.com | Mobile: 8282864451", subtitle_style))
    story.append(Paragraph("<b><u>RESIDENCE VERIFICATION REPORT</u></b>", ParagraphStyle('H2', parent=title_style, fontSize=11, textColor=colors.HexColor('#222222'))))
    story.append(Spacer(1, 6))
    
    data = [
        [Paragraph("<b>Branch Name:</b>", styles['Normal']), Paragraph(branch_name, styles['Normal']), Paragraph("<b>Lifting Date:</b>", styles['Normal']), Paragraph(lifting_date, styles['Normal'])],
        [Paragraph("<b>Applicant Name:</b>", styles['Normal']), Paragraph(applicant_name, styles['Normal']), Paragraph("<b>Date of Visit:</b>", styles['Normal']), Paragraph(date_of_visit)],
        [Paragraph("<b>Address:</b>", styles['Normal']), Paragraph(address, styles['Normal']), Paragraph("<b>Time of Visit:</b>", styles['Normal']), Paragraph(time_of_visit)],
        [Paragraph("<b>Address Confirmed:</b>", styles['Normal']), Paragraph(address_confirmed, styles['Normal']), Paragraph("<b>Person Met:</b>", styles['Normal']), Paragraph(person_met)],
        [Paragraph("<b>Relationship:</b>", styles['Normal']), Paragraph(relationship, styles['Normal']), Paragraph("<b>Marital Status:</b>", styles['Normal']), Paragraph(marital_status)],
        [Paragraph("<b>Family / Earning:</b>", styles['Normal']), Paragraph(f"Family: {family_members} | Earning: {earning_members}", styles['Normal']), Paragraph("<b>Children:</b>", styles['Normal']), Paragraph(children)],
        [Paragraph("<b>Spouse Working:</b>", styles['Normal']), Paragraph(is_spouse_working, styles['Normal']), Paragraph("<b>Details:</b>", styles['Normal']), Paragraph(spouse_details)],
        [Paragraph("<b>Ownership:</b>", styles['Normal']), Paragraph(ownership, styles['Normal']), Paragraph("<b>Years in House:</b>", styles['Normal']), Paragraph(years_in_house)],
        [Paragraph("<b>Construction:</b>", styles['Normal']), Paragraph(construction, styles['Normal']), Paragraph("<b>Roof Type:</b>", styles['Normal']), Paragraph(roof_type)],
        [Paragraph("<b>Approx Area:</b>", styles['Normal']), Paragraph(approx_area, styles['Normal']), Paragraph("<b>Floor:</b>", styles['Normal']), Paragraph(floor)],
        [Paragraph("<b>Assets Seen:</b>", styles['Normal']), Paragraph(assets_seen, styles['Normal']), Paragraph("<b>Vehicle:</b>", styles['Normal']), Paragraph(vehicle)],
        [Paragraph("<b>Political Portrait:</b>", styles['Normal']), Paragraph(portrait, styles['Normal']), Paragraph("<b>Purpose:</b>", styles['Normal']), Paragraph(purpose)],
        [Paragraph("<b>Loans Taken:</b>", styles['Normal']), Paragraph(loans_taken, styles['Normal']), Paragraph("<b>Financier / EMI:</b>", styles['Normal']), Paragraph(f"{financier} / {emi}")],
        [Paragraph("<b>Neighbor Feedback:</b>", styles['Normal']), Paragraph(neighbors_feedback, styles['Normal']), Paragraph("<b>Remarks:</b>", styles['Normal']), Paragraph(f"<b><font color='green'>{remarks}</font></b>")],
        [Paragraph("<b>Recommendation:</b>", styles['Normal']), Paragraph(recommendation, styles['Normal']), Paragraph("<b>Status:</b>", styles['Normal']), Paragraph("Positive")]
    ]
    
    t = Table(data, colWidths=[110, 160, 100, 190])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F9F9F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CCCCCC')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DDDDDD')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph(f"<b>Verifier Remarks:</b> {verifier_remarks}", styles['Normal']))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("<b>Verification Photos:</b>", styles['Heading2']))
    story.append(Spacer(1, 4))
    
    img_data = []
    temp_files = []
    
    for idx, up_file in enumerate([uploaded_photo1, uploaded_photo2]):
        if up_file is not None:
            temp_path = f"temp_img_{idx}.jpg"
            with open(temp_path, "wb") as f:
                f.write(up_file.getbuffer())
            temp_files.append(temp_path)
            img_data.append(RLImage(temp_path, width=250, height=170))
            
    if len(img_data) > 0:
        while len(img_data) < 2:
            img_data.append("")
        photo_table = Table([[img_data[0], img_data[1]]], colWidths=[280, 280])
        photo_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(photo_table)

    story.append(Spacer(1, 10))
    
    # Seal আৰু Verifier Name ৰ সঠিক বিন্যাস (যাতে চীলটো ভেৰিফাইয়াৰ নামৰ ওপৰত বা কাষত মিলে)
    seal_element = ""
    if uploaded_seal is not None:
        seal_path = "temp_seal.png"
        with open(seal_path, "wb") as f:
            f.write(uploaded_seal.getbuffer())
        temp_files.append(seal_path)
        seal_element = RLImage(seal_path, width=90, height=90)
    else:
        seal_element = Paragraph("<b>[ Seal Placeholder ]</b>", styles['Normal'])

    sig_layout_data = [
        [seal_element, Paragraph(f"<b>Verifier Name: - {verifier_name}</b><br/><br/><b>Authorized Signature with Seal</b>", styles['Normal'])]
    ]
    sig_table = Table(sig_layout_data, colWidths=[150, 410])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(sig_table)

    doc.build(story)
    pdf_buffer.seek(0)
    
    # --- Word Generation ---
    doc_word = Document()
    doc_word.add_heading("TIGER 4 INDIA LIMITED", level=1)
    doc_word.add_paragraph("Corporate Office: #7, Lower Ground Floor, L.S.C., B-1, Vasant Kunj, New Delhi-110070 India\nE-mail id: tigindialtd@gmail.com | Mobile: 8282864451")
    doc_word.add_heading("RESIDENCE VERIFICATION REPORT", level=2)
    doc_word.add_paragraph(f"Branch Name: {branch_name} | Lifting Date: {lifting_date}")
    doc_word.add_paragraph(f"Name of Applicant: {applicant_name}")
    doc_word.add_paragraph(f"Residence Address: {address}")
    doc_word.add_paragraph(f"Date of Visit: {date_of_visit} | Time: {time_of_visit}")
    doc_word.add_paragraph(f"Person Met: {person_met} ({relationship})")
    doc_word.add_paragraph(f"Family Members: {family_members} | Earning: {earning_members}")
    doc_word.add_paragraph(f"Ownership: {ownership} | Construction: {construction} | Roof: {roof_type}")
    doc_word.add_paragraph(f"Verifier Remarks: {verifier_remarks}")
    doc_word.add_paragraph(f"\nVerifier Name: - {verifier_name}\nAuthorized Signature with Seal")
    
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
