from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_ollama import ChatOllama
from langchain.output_parsers import PydanticOutputParser
from typing import List
from pydantic import BaseModel


class review(BaseModel):
    subject : str
    body : str

parser = PydanticOutputParser(pydantic_object=review)    


def generate_email(candidate_name, jd_summary,date,sender_name,sender_posi,sender_comp):
    prompt = PromptTemplate(template="""
        Write a subject and body of professional interview invitation email for {candidate_name} , with date and timings - {date}  for a role described in:
        {jd_summary} ,dont write anything about responsibilities only write for role assigned also it should be short and consise.
                            and tell further round info will be told after completion of this round.
                            by following sender details: name of sender :{sender_name} 
                                                         position : {sender_posi}
                                                         company name : {sender_comp}
                            and  Extract the following details in JSON format with these keys:\n
        {format_instructions}\n\n 
                            
    """,
    input_variables=['candidate_name','date','jd_summary','sender_name','sender_posi','sender_comp'],
    partial_variables={"format_instructions":parser.get_format_instructions()})
    llm = ChatOllama(model='mistral')
    chain= prompt | llm | parser
    return chain.invoke({'candidate_name':candidate_name,'jd_summary':jd_summary,'date':date,'sender_name':sender_name,'sender_posi':sender_posi,'sender_comp':sender_comp})


# text= """
# {
#       "skills": ["Data Analysis", "Machine Learning", "Statistical Analysis", "Predictive Modeling", "Data Mining", "Pattern Recognition", "Experimentation", "A/B Testing", "Data Visualization", "Programming (Python, R etc.)", "Cross-functional Collaboration", "Communication"],
#       "work_exp": "Proven experience in data science, machine learning, or predictive analytics roles.",
#       "imp_keywords": ["Data Scientist", "Machine Learning", "Predictive Modeling", "Data Analysis", "Advanced Degree", "Programming Languages", "Statistical Analysis", "Data Visualization"],
#       "edu_qual": "Advanced degree (Master's or Ph.D.) in Computer Science, Statistics, Mathematics, Economics, or related field.",
#       "summary": "We are seeking a Data Scientist with advanced degrees and experience in data science, machine learning, or predictive analytics roles. The candidate will utilize their analytical skills to extract insights from complex datasets, develop predictive models, collaborate cross-functionally, and solve challenging business problems."
#    }
# """

# print(generate_email('arun',text,"2023-2-3 12:00AM",'sakshi','HR','google'))
