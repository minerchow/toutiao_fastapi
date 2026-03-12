#检查收藏状态 当前用户是否收藏了该新闻
from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.favorite import Favorite
from models.news import News

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
   # select (查询主体模型类).join(联合查询的模型类，联合查询的条件).where().order_by()
   query = (select(News,Favorite.created_at.label('favorite_time'),Favorite.id.label('favorite_id'))
            .join(Favorite,News.id == Favorite.news_id)
            .where(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
   result = await db.execute(query)
   rows = result.all()
   return rows,total

 # 删除所有收藏
async def clear_favorites(db: AsyncSession, user_id: int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0
      
