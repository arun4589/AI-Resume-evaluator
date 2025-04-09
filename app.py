import streamlit as st
from datetime import datetime
from src.utils.file_handler import save_uploaded_files
from src.agents.email_sender import send_email
from src.parser.JD_parser import parse_jd
from src.parser.resume_parser import parse_resume
from src.agents.JD_summeriser import summarize_jd
from src.agents.resume_evaluator import evaluate_resume
from src.agents.shortlister import shortlist_candidates
from src.agents.email_generator import generate_email

# Page config
st.set_page_config(page_title="AI Resume Evaluator", page_icon="🧠", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #4A90E2;'>🧠 AI Resume Evaluator</h1>",
    unsafe_allow_html=True,
)

st.markdown("---")

# Upload Section
with st.container():
    st.subheader("📄 Upload Files")
    col1, col2 = st.columns(2)
    
    with col1:
        jd_file = st.file_uploader("**Upload Job Description (PDF)**", type="pdf")
    with col2:
        resumes = st.file_uploader("**Upload Resumes (PDFs)**", type="pdf", accept_multiple_files=True)

# Email Details Section
with st.expander("📧 Enter Email & Interview Details", expanded=True):
    st.markdown("Fill in the following fields to send interview invites to shortlisted candidates:")
    
    col1, col2 = st.columns(2)
    with col1:
        sender_name = st.text_input("🧑‍💼 Your Name")
        sender_posi = st.text_input("💼 Your Position")
        sender_email = st.text_input("📨 Your Email")
        date = st.date_input("🗓️ Interview Date")
    with col2:
        sender_comp = st.text_input("🏢 Your Company")
        sender_pass = st.text_input("🔐 Email Password", type="password")
        time = st.time_input("⏰ Interview Time")

    comb = datetime.combine(date=date, time=time)

# Evaluation Section
st.markdown("---")
st.subheader("📝 Evaluation and Shortlisting")

if st.button("🚀 Evaluate Candidates"):
    if jd_file and resumes:
        with st.spinner("🔍 Parsing Job Description..."):
            jd_text = parse_jd(jd_file)
            jd_summary = summarize_jd(jd_text)

        with st.spinner("📂 Parsing Resumes & Evaluating..."):
            resume_texts = [parse_resume(resume) for resume in resumes]
            results = [evaluate_resume(text, jd_summary) for text in resume_texts]

        with st.spinner("✅ Shortlisting Candidates..."):
            shortlisted = shortlist_candidates(results)

        st.success("🎉 Evaluation Completed!")

        st.markdown("### ✅ **Shortlisted Candidates**")
        for result in shortlisted:
           bg_color = "#e0ebff" if result['shortlist_status'] == "YES" else "#ffe6e6"
           text_color = "#000000"
           status_color = "green" if result['shortlist_status'] == "YES" else "red"
           st.markdown(
               f"""
               <div style="padding: 15px; background-color: {bg_color}; border-radius: 12px; 
                           margin-bottom: 10px; color: {text_color}; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <strong>👤 Candidate:</strong> {result['name']}<br>
                    <strong>📊 Score:</strong> {result['score']}<br>
                    <strong>📌 Status:</strong> <span style="color: {status_color}; font-weight: bold;">{result['shortlist_status']}</span>
               </div>
                """,
                unsafe_allow_html=True,
             )
        if result['shortlist_status'] == "YES":
                with st.spinner(f"📤 Sending email to {result['name']}..."):
                    email_setup = generate_email(result['name'], jd_summary, comb, sender_name, sender_posi, sender_comp)
                    send_email(
                        to_email=result['email'],
                        subject=email_setup.subject,
                        body=email_setup.body,
                        from_email=sender_email,
                        password=sender_pass,
                    )
        st.balloons()

    else:
        st.warning("⚠️ Please upload both a job description and at least one resume.")






