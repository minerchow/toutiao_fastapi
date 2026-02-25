from fastapi import FastAPI
from routers import news
from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI实例
app = FastAPI()

# 设置跨域option
options = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
app.add_middleware(
    CORSMiddleware,
    allow_origins=options["allow_origins"],
    allow_credentials=options["allow_credentials"],
    allow_methods=options["allow_methods"],
    allow_headers=options["allow_headers"],
)

# 包含路由
app.include_router(news.router)

@app.get("/")
async def root():
    return {"msg":"hello toutiao-fastapi"}
