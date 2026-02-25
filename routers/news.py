from fastapi import APIRouter,Depends,Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news
from config.db_conf import get_db 


# 创建apiRouter
router = APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # 先获取数据库里面新闻分类数据 → 先定义模型类 → 封装查询数据的方法
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }

@router.get("/list")
async def get_news_list(
    category_id: int = Query(...,alias="categoryId"),
    page:int = 1,
    page_size:int = Query(10,alias="pageSize",le=100),
    db: AsyncSession = Depends(get_db)
):
    # 先获取数据库里面新闻数据 → 先定义模型类 → 封装查询数据的方法
    news_list = await news.get_news_list(db, category_id, (page - 1) * page_size, page_size)
    total = await news.get_news_count(db, category_id)
    # hasMore 跳过的 + 当前列表数量 < 总量
    has_more = (page - 1) * page_size + len(news_list) < await news.get_news_count(db, category_id)
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list":news_list,
            "total": total,
            "hasMore":   has_more
        }
    }

@router.get("/detail")
async def get_news_detail(
    news_id: int = Query(...,alias="newsId"),
    db: AsyncSession = Depends(get_db)
):
    # 先获取数据库里面新闻数据 → 先定义模型类 → 封装查询数据的方法
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return {
        "code": 200,
        "message": "获取新闻详情成功",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publishTime":news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views":news_detail.views,
            "relatedNews":[]
        }
    }
    
