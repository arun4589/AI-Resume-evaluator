from langchain.prompts import PromptTemplate
from typing import Annotated,Optional,Literal,TypedDict
from pydantic import Field, BaseModel
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser


parser = StrOutputParser()




def summarize_jd(jd_text):
    prompt = PromptTemplate(template="""summarise the following given JOB description in important points :  {jd_text}""",
                            input_variables=['jd_text'])
    llm = ChatOllama(model="mistral")
    chain = prompt | llm | parser
    return chain.invoke({'jd_text':jd_text})





# from langchain.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from utils.llm_connector import get_llm
# from db.database import insert_jd

# parser = StrOutputParser()

# def summarize_jd(jd_text: str) -> str:
#     prompt = PromptTemplate(
#         template="Summarise the following JOB description into key bullet points:\n\n{jd_text}",
#         input_variables=['jd_text']
#     )
    
#     llm = get_llm(model_name="mistral")
#     chain = prompt | llm | parser
#     jd_summary = chain.invoke({'jd_text': jd_text})

#     # Save into DB
#     insert_jd(jd_text, jd_summary)

#     return jd_summary




