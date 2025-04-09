from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain.output_parsers import PydanticOutputParser
from typing import List
from pydantic import BaseModel


class review(BaseModel):
    name : str
    score : int
    phone : str
    email : str
    summary : str
    

parser=PydanticOutputParser(pydantic_object=review)


def evaluate_resume(resume_text, jd_summary):
    prompt = PromptTemplate(template="""
        Given the job summary:
        {jd_summary}

        And the resume:
        {resume_text}

        Evaluate this candidate on a scale of 0–100 for fit and Extract the following details in JSON format with these keys:\n
        {format_instructions}\n\n                                  
                            
    """,
    input_variables=['jd_summary','resume_text'],
    partial_variables={'format_instructions':parser.get_format_instructions()})


    llm = ChatOllama(model="mistral")
    chain = prompt | llm | parser
    
    return chain.invoke({
    "jd_summary": jd_summary,
    "resume_text": resume_text
})


