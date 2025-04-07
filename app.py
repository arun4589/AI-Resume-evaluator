import streamlit as st
from src.utils.file_handler import save_uploaded_files
from src.parser.JD_parser import parse_jd
from src.parser.resume_parser import parse_resume
from src.agents.JD_summeriser import summarize_jd
from src.agents.resume_evaluator import evaluate_resume
from src.agents.shortlister import shortlist_candidates
from src.agents.email_generator import generate_email

st.title("🧠 AI Resume Evaluator")

# Upload JD
jd_file = st.file_uploader("Upload Job Description (PDF)", type="pdf")
# Upload multiple resumes
resumes = st.file_uploader("Upload Resumes (PDF)", type="pdf", accept_multiple_files=True)

if st.button("Evaluate"):
    if jd_file and resumes:
        jd_text = parse_jd(jd_file)
        jd_summary = summarize_jd(jd_text)

        resume_texts = [parse_resume(resume) for resume in resumes]
        results = [evaluate_resume(text, jd_summary) for text in resume_texts]

        shortlisted = shortlist_candidates(results)

        st.subheader("Shortlisted Candidates")
        for result in shortlisted:
            st.markdown(f"**Candidate:** {result['name']} - Score: {result['score']}")
            st.write(result['summary'])
            st.write(generate_email(result['name'], jd_summary))

    else:
        st.warning("Please upload both a job description and at least one resume.")
