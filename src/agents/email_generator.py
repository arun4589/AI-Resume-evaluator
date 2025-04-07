from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.utils.llm_connector import get_llm

def generate_email(candidate_name, jd_summary):
    prompt = PromptTemplate.from_template("""
        Write a professional interview invitation email for {candidate_name} for a role described as:
        {jd_summary}
    """)
    chain = LLMChain(prompt=prompt, llm=get_llm())
    return chain.run(candidate_name=candidate_name, jd_summary=jd_summary)
