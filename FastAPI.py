from datetime import datetime
import os
from uuid import uuid4
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

# LLM模型引入
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import ChatGLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

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

def turboModel():
    model = ChatOpenAI(model = "gpt-3.5-turbo")
    model.openai_api_key = "EMPTY"
    model.openai_api_base = "http://10.58.0.2:6677/v1"
    return model

def glmModel():
    model = ChatOpenAI(model = "gpt-3.5-turbo")
    model.openai_api_key = "EMPTY"
    model.openai_api_base = "http://10.58.0.2:7681/v1"
    return model

def openaiEmbedding():
    model = OpenAIEmbeddings()
    model.openai_api_key = ""
    model.openai_api_base = "https://api.openai.com/v1"
    return model

print("模型已确认")

# MD导入
from langchain.document_loaders import UnstructuredMarkdownLoader
import re

def loadMD(path):
    loader = UnstructuredMarkdownLoader(path)
    document = loader.load()
    con = document[0].page_content.replace("\n\n","\n")
    pattern = r'\\u[0-9]{4}'
    result = re.sub(pattern, " ", con)
    return result

# 文档结构解析
import re
import json

def parseDocument(con):
    headings = []
    current_heading = None

    for line in con:
        line = line.strip()
        if re.match(r'^\d+(\.\d+)*\s+', line):
            if current_heading:
                headings.append(current_heading)
            level, title = re.split(r'\s+', line, maxsplit=1)
            current_heading = {
                'level': level,
                'title': title,
                'content': ""
            }
        else:
            if current_heading:
                current_heading['content']+=line+"\n"

    if current_heading:
        headings.append(current_heading)

    l = len(headings)
    for i in range(l):
        for j in range(i):
            if headings[i-j-1]["level"].split(".") == headings[i]["level"].split(".")[0:len(headings[i]["level"].split("."))-1]:
                headings[i]["title"] = headings[i-j-1]["title"] + " " + headings[i]["title"]

    headings = [heading for heading in headings if heading["content"]!=""]
    print("文本已解析")
    return headings

#requirements_json = parseDocument(loadMD(r"D:\Lessons\Graduate\Tutor\erp-backend\需求规格说明文档.md").split('\n'))


# 嵌入模型生成
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

def makeRetriever(requirements_json):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = []

    for i in range(len(requirements_json)):
        texts += text_splitter.split_text(requirements_json[i]["title"]+"\n"+requirements_json[i]["content"])
    #texts = text_splitter.split_text(full_text)

    #embeddings = OpenAIEmbeddings()
    # embeddings = OpenAIEmbeddings(openai_api_base="http://10.58.0.2:6678/v1", openai_api_key= "xx")
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    docs = []
    for i in range(len(requirements_json)):
        docs.append(Document(page_content=requirements_json[i]["title"]+"\n"+requirements_json[i]["content"], metadata={"title":requirements_json[i]["title"]}))

    #print(docs)
    #db = Chroma.from_texts(texts, embeddings)
    db = Chroma.from_documents(docs, embeddings)

    retriever = db.as_retriever()
    print("嵌入已完成")
    return retriever



# 对话模板
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

def makeChain(retriever):
    template = """
    你是某软件项目的测试人员，需要根据需求规格说明文档的内容编写测试用例。接下来我会给出相关的需求规格文档，而你将根据其写出对应的测试用例。
    要求测试用例格式为用严格合法json的形式，并要求包括案例序号，案例名称，描述，参与者，触发条件，前置条件，后置条件，正常流程，预期值。其中正常流程尽可能写全面点。
    下面是相关的需求规格文档：
    {context}

    要求写出 {question}的测试用例
    """
    prompt = ChatPromptTemplate.from_template(template)
    model = openaiModel()

    if retriever is None:
        chain = (
            {"context": lambda *args, **kwargs: "", "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        return chain
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain



# 返回json解析
import json

def parseJson(answer):
    left = answer.index("{")
    right = answer.index("{")
    output = []
    cnt = 1
    
    while(left<len(answer) and right<len(answer)):
        right+=1
        if right>=len(answer):
            print(answer)
            return output
        if answer[right] == "}":
            cnt-=1
        if answer[right] == "{":
            cnt+=1
        if cnt==0:
            try:
                answer_json = json.loads(answer[left:right+1].replace("\n", "").replace("  ", "").replace("，",",").replace("。",".").replace("\\","").replace(",}","}").replace("'",'"'))    
                if len(answer_json.keys())==1:
                    answer_json = answer_json[list(answer_json.keys())[0]]
                output.append(answer_json)
            except:
                print(f"error from:{left} to {right}")
                print(answer[left:right+1])
                print()
            left = right+1
            while(left<len(answer) and answer[left]!="{"):
                left+=1
            cnt = 1
    if len(output)==1:
        return output[0]
    return output


# FastAPI
app = FastAPI()
chain = makeChain(None)

@app.get("/")
def read_root():
    return {"message": "Hello, World"}

class ChatRequest(BaseModel):
    message: str
    
@app.post("/useCase/chat")
def processText(long_text: ChatRequest):
    # 处理传递的长文本数据
    message = long_text.message
    print(f"对话：{message}")
    # 进行文本处理逻辑
    ans = chain.invoke(message)  # 这里只是一个示例
    print(f"回答：{ans}")
    print()
    response = parseJson(ans)
    return response

@app.post("/useCase/retriever")
async def uploadRetriver(file: UploadFile = File(...)):
    global chain
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid4())
    if file.filename:
        file_extension = file.filename.split(".")[-1]
        new_filename = f"{timestamp}_{unique_id}.{file_extension}"
        file_path = os.path.join("upload_folder", new_filename)
        with open(file_path, "wb") as file_object:
            file_object.write(file.file.read())
        requirements_json = parseDocument(loadMD(file_path).split('\n'))
        print(requirements_json)
        retriever = makeRetriever(requirements_json)
        chain = makeChain(retriever)
        return {"message":"Success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
