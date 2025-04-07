from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.utils.llm_connector import get_llm

def evaluate_resume(resume_text, jd_summary):
    prompt = PromptTemplate.from_template("""
        Given the job summary:
        {jd_summary}

        And the resume:
        {resume_text}

        Evaluate this candidate on a scale of 0–100 for fit. Return:
        - Name
        - Score
        - Summary of match
    """)
    chain = LLMChain(prompt=prompt, llm=get_llm())
    return chain.run(jd_summary=jd_summary, resume_text=resume_text)
