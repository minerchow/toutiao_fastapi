#检查收藏状态 当前用户是否收藏了该新闻
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.favorite import Favorite
async def is_new_favorite(db: AsyncSession, user_id, news_id: int):
    # 查询用户是否收藏了该新闻
    query = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(query)
    #
    return result.scalars().one_or_none() is not None

async def add_new_favorite(db: AsyncSession, user_id, news_id: int):
    # 创建收藏记录
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

async def remove_new_favorite(db: AsyncSession, user_id, news_id: int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
        