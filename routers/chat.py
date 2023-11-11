# todo: 聊天接口

from fastapi import APIRouter

chat_router = APIRouter(prefix='/chat')

@chat_router.post("/")
async def foo():
    return {"message": "unimplemented"}