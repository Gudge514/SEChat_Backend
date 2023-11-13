# api前缀与端口号
API_PREFIX = '/v1'
PORT = 11451

# 日志
import logging
logging.basicConfig(
    level=logging.INFO,
    format="\n[%(asctime)s - {%(module)s.py (%(lineno)d)} - %(funcName)s()]\n %(message)s\n",
    datefmt="%Y-%m-%d,%H:%M:%S",
)

# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 处理跨域请求
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
from routers import use_case_router
app.include_router(use_case_router, prefix=API_PREFIX)


# 服务器根应答
@app.get("/")
def read_root():
    return {"message": "Hello, World"}


# 程序入口
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, workers=1)