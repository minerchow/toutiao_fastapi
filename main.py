from fastapi import FastAPI
from routers import news

# 创建FastAPI实例
app = FastAPI()

# 包含路由
app.include_router(news.router)

@app.get("/")
async def root():
    return {"msg":"hello toutiao-fastapi"}
