if "generated_files" not in st.session_state:
    st.session_state.generated_files = None

if submitted:
    missing_fields = []
    if not branch_name.strip():
        missing_fields.append("Branch Name")
    if not lifting_date.strip():
        missing_fields.append("Lifting Date")
    if not applicant_name.strip():
        missing_fields.append("Name of Applicant")
    if not customer_mobile.strip():
        missing_fields.append("Customer Mobile Number")
    if not address.strip():
        missing_fields.append("Residence Address")
    if not date_of_visit.strip():
        missing_fields.append("Date of Visit")
    if not time_of_visit.strip():
        missing_fields.append("Time of Visit")
    if not relationship.strip():
        missing_fields.append("Relationship")
    if not person_met.strip():
        missing_fields.append("Person Met")

    if missing_fields:
        st.error(
            f"❌ Please fill out all mandatory fields marked with (*): {', '.join(missing_fields)}"
        )
    else:
        if solar_install == "No":
            final_verifier_remarks = (
                f"I Visited At The Provided Address & I Met with {person_met} Confirmed His Address. "
                "Neighbor’s feedback Is Satisfactory. There is no Adverse report found as per enquiry. "
                "Hence The Residence Report is Positive."
            )
        else:
            final_verifier_remarks = (
                "I Visited At The Provided Address and found solar panel is successfully installed"
            )

        current_data = {
            "branch_name": branch_name,
            "lifting_date": lifting_date,
            "applicant_name": applicant_name,
            "customer_mobile": customer_mobile,
            "occupation": occupation,
            "address": address,
            "date_of_visit": date_of_visit,
            "time_of_visit": time_of_visit,
            "address_confirmed": address_confirmed,
            "person_met": person_met,
            "relationship": relationship,
            "marital_status": marital_status,
            "family_members": family_members,
            "earning_members": earning_members,
            "children": children,
            "is_spouse_working": is_spouse_working,
            "spouse_details": spouse_details,
            "ownership": ownership,
            "years_in_house": years_in_house,
            "construction": construction,
            "roof_type": roof_type,
            "approx_area": approx_area,
            "floor": floor,
            "assets_seen": assets_seen,
            "vehicle": vehicle,
            "portrait": portrait,
            "purpose": purpose,
            "financier": financier,
            "emi": emi,
            "loans_taken": loans_taken,
            "neighbor_name": neighbor_name,
            "neighbor_mobile": neighbor_mobile,
            "neighbors_feedback": neighbors_feedback,
            "solar_install": solar_install,
            "remarks": remarks,
            "verifier_name": verifier_name,
            "final_verifier_remarks": final_verifier_remarks,
        }

        pdf_buffer, word_buffer = generate_report_files(
            current_data, uploaded_photo1, uploaded_photo2, uploaded_seal
        )

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_record = {
            "Timestamp": current_time,
            "Applicant Name": applicant_name,
            "Branch Name": branch_name,
            "Customer Mobile": customer_mobile,
            "FullData": current_data,
        }

        st.session_state.report_history.append(new_record)
        save_history(st.session_state.report_history)

        safe_applicant_name = "".join(c if c.isalnum() else "_" for c in applicant_name)
        safe_branch_name = "".join(c if c.isalnum() else "_" for c in branch_name)
        file_prefix = f"{safe_applicant_name}_{safe_branch_name}"

        st.session_state.generated_files = {
            "pdf": pdf_buffer.getvalue(),
            "word": word_buffer.getvalue(),
            "pdf_name": f"{file_prefix}_Report.pdf",
            "word_name": f"{file_prefix}_Report.docx",
        }

if st.session_state.generated_files is not None:
    st.success("✨ Files successfully generated! Tolor download button click kori file namai lobo pare:")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            "📥 Download PDF",
            data=st.session_state.generated_files["pdf"],
            file_name=st.session_state.generated_files["pdf_name"],
            mime="application/pdf",
            key="download_generated_pdf",
        )
    with col_d2:
        st.download_button(
            "📥 Download Word",
            data=st.session_state.generated_files["word"],
            file_name=st.session_state.generated_files["word_name"],
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key="download_generated_word",
        )
