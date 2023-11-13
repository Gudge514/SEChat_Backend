# 网络请求
from fastapi import APIRouter, File, UploadFile

# 数据结构
from utils.data import ChatRequest

# 工具库
from datetime import datetime
import os
from uuid import uuid4

# 日志
import logging
logger = logging.getLogger(__name__)

from internal.template import makeChain
chain = makeChain(None)

use_case_router = APIRouter(prefix='/useCase')

@use_case_router.post("")
async def processText(long_text: ChatRequest):
    global chain
    
    # 文本模版
    
    # 解析器
    from utils.parser import parseJson
    
    # 处理传递的长文本数据
    message = long_text.message
    logger.info(f"对话：{message}")
    # 进行文本处理逻辑
    ans = chain.invoke(message)  # 这里只是一个示例
    logger.info(f"回答：{ans}")
    
    response = parseJson(ans)
    return response

@use_case_router.post("/retriever")
async def uploadRetriver(file: UploadFile = File(...)):
    global chain
    
    # 加载器
    from utils.loader import loadMD
    
    # 解析器
    from utils.parser import parseDocument
    
    # 文本模版
    from internal.template import makeChain    
    # 寻回模型加载
    from internal.retriever import makeRetriever
    
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid4())
    
    if file.filename:
        file_extension = file.filename.split(".")[-1]
        new_filename = f"{timestamp}_{unique_id}.{file_extension}"
        file_path = os.path.join("upload_folder", new_filename)
        print(file_path)
        
        with open(file_path, "wb") as file_object:
            file_object.write(file.file.read())
            
        requirements_json = parseDocument(loadMD(file_path).split('\n'))
        logger.info(requirements_json)
        
        retriever = makeRetriever(requirements_json)
        chain = makeChain(retriever)
        
        return {"message":"Success"}