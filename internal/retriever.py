# 使用数据库
from langchain.vectorstores import Chroma

# 嵌入模型生成
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

# 日志
import logging
logger = logging.getLogger(__name__)

def makeRetriever(requirements_json):
    
    # 选择嵌入模型
    from internal.model import getEmbeddingByName
    embeddings = getEmbeddingByName(name="m3e-large")
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = []

    for i in range(len(requirements_json)):
        texts += text_splitter.split_text(requirements_json[i]["title"]+"\n"+requirements_json[i]["content"])
    #texts = text_splitter.split_text(full_text)

    # embeddings = OpenAIEmbeddings()
    # embeddings = OpenAIEmbeddings(openai_api_base="http://10.58.0.2:6678/v1", openai_api_key= "xx")
    # embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    docs = []
    for i in range(len(requirements_json)):
        docs.append(Document(page_content=requirements_json[i]["title"]+"\n"+requirements_json[i]["content"], metadata={"title":requirements_json[i]["title"]}))

    #print(docs)
    #db = Chroma.from_texts(texts, embeddings)
    db = Chroma.from_documents(docs, embeddings)

    retriever = db.as_retriever()
    logger.info("嵌入已完成")
    return retriever