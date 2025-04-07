from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.utils.llm_connector import get_llm

def summarize_jd(jd_text):
    prompt = PromptTemplate.from_template("""
        Summarize the following job description into 5 key points:
        {jd_text}
    """)
    chain = LLMChain(prompt=prompt, llm=get_llm())
    return chain.run(jd_text=jd_text)
