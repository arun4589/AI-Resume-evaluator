from langchain_community.chat_models import ChatOllama

def get_llm(model_name="mistral"):
    return ChatOllama(model=model_name)
