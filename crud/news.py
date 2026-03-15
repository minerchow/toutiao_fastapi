
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from models.news import Category,News
from sqlalchemy import select,func,update
from cache.news_cache import get_cached_categories,set_cached_categories,get_cache_news_list,set_cached_categories_list

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    # 先从缓存中获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    # 写入缓存
    if categories:
        categories = jsonable_encoder(categories)
        await set_cached_categories(categories)
    return categories

async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    page = skip // limit + 1
    # 从缓存中获取数据
    cached_news_list = await get_cache_news_list(category_id, page, limit) #json
    if cached_news_list:
        # cached_news_list转成orm模型
        cached_news_list = [News(**item) for item in cached_news_list]
        return cached_news_list
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()
    #写入缓存
    if news_list:
        news_list = jsonable_encoder(news_list)
        await set_cached_categories_list(category_id, page, limit, news_list, expire=600)
    return news_list

async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one() #只能返回一个值

async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increment_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    # 检查是否真的命中，命中返回true
    return result.rowcount > 0

async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 10):
    #orderBy 发布时间和浏览量
    stmt = select(News).where(News.category_id == category_id, News.id != news_id).order_by(News.publish_time.desc(),News.views.desc()).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    # 返回前端只要id title content image author publishTime views
    return [{
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "image": news.image,
        "author": news.author,
        "publishTime": news.publish_time,
        "views": news.views
    } for news in related_news]

