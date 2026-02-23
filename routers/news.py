from fastapi import APIRouter
# 创建apiRouter
router = APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_categories():
    return {"msg":"获取分类信息成功"}