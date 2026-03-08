#检查收藏状态 当前用户是否收藏了该新闻
from sqlalchemy import func, select, delete
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

#  获取收藏列表 获取的是某个用户收藏列表 + 分页
async def get_favorite_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
   count_query = select(func.count()).select_from(Favorite).where(Favorite.user_id == user_id)
   count_result = await db.execute(count_query)
   total = count_result.scalar_one()
        
   # 收藏列表 连表查询 + 分页 + 收藏时间排序     
