from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

# accessible model
def openaiModel():
    model = ChatOpenAI(model = "gpt-3.5-turbo")
    model.openai_api_key = ""
    model.openai_api_base = "https://api.openai.com/v1"
    return model

def llamaModel():
    model = ChatOpenAI(model = "CodeLlama-34b-Chat")
    model.openai_api_key = "EMPTY"
    model.openai_api_base = "http://10.58.0.2:8000/v1"
    return model

def baichuanModel():
    model = ChatOpenAI(model = "baichuan2-13b-chat")
    model.openai_api_key = "EMPTY"
    model.openai_api_base = "http://10.58.0.2:6677/v1"
    return model

def glmModel():
    model = ChatOpenAI(model = "chatglm3-6b", openai_api_key="xxx", openai_api_base="http://10.58.0.2:6678/v1")
    return model

def openaiEmbedding():
    model = OpenAIEmbeddings()
    model.openai_api_key = ""
    model.openai_api_base = "https://api.openai.com/v1"
    return model

def m3eEmbedding():
    model = OpenAIEmbeddings(openai_api_key="xxx", openai_api_base="http://10.58.0.2:6678/v1")
    return model


# 允许工具利用模型名字这一参数自动获取模型对象
def getModelByName(name: str):
    
    pass