
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category,News
from sqlalchemy import select,func
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
   stmt = select(Category).offset(skip).limit(limit)
   result = await db.execute(stmt)
   return result.scalars().all()

async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one() #只能返回一个值

async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
    
