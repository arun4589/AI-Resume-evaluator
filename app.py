import streamlit as st
from src.utils.file_handler import save_uploaded_files
from src.agents.email_sender import send_email
from src.parser.JD_parser import parse_jd
from src.parser.resume_parser import parse_resume
from src.agents.JD_summeriser import summarize_jd
from src.agents.resume_evaluator import evaluate_resume
from src.agents.shortlister import shortlist_candidates
from src.agents.email_generator import generate_email
from datetime import datetime

st.title("🧠 AI Resume Evaluator")

# Upload JD
jd_file = st.file_uploader("Upload Job Description (PDF)", type="pdf")
# Upload multiple resumes
resumes = st.file_uploader("Upload Resumes (PDF)", type="pdf", accept_multiple_files=True)

st.text("INPUT the following details for email ")
sender_name=st.text_input("Enter Your Name")
sender_posi=st.text_input("Your position")
sender_comp=st.text_input("your company name")
sender_email = st.text_input("Enter your email")
sender_pass = st.text_input("enter password of your email")
date=st.date_input("enter date for interview")
time=st.time_input('enter time for interview')
comb = datetime.combine(date=date,time=time)

if st.button("Evaluate"):
    if jd_file and resumes:
        jd_text = parse_jd(jd_file)
        jd_summary = summarize_jd(jd_text)

        resume_texts = [parse_resume(resume) for resume in resumes]
        results = [evaluate_resume(text, jd_summary) for text in resume_texts]

        shortlisted = shortlist_candidates(results)

        st.subheader("Shortlisted Candidates")
       
        for result in shortlisted:
            st.markdown(f"**Candidate:** {result['name']} - Score: {result['score']} - Shortlist status : {result['shortlist_status']}")
            if result['shortlist_status']=="YES":
              email_setup = generate_email(result['name'], jd_summary,comb,sender_name,sender_posi,sender_comp)
              send_email(to_email=result['email'],
                         subject=email_setup.subject,
                         body=email_setup.body,
                         from_email=sender_email,
                         password=sender_pass)

    else:
        st.warning("Please upload both a job description and at least one resume.")
