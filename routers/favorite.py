from fastapi import APIRouter, Depends, HTTPException, status,Query,Body
from models.users import User
from utils.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud.favorite import is_new_favorite,add_new_favorite,remove_new_favorite,get_favorite_list,clear_favorites
from utils.response import success_response
from schemas.favorite import FavoriteCheckRequest,FavoriteAddRequest,FavoriteListResponse
router = APIRouter(prefix="/api/favorite",tags=["favorite"])

@router.get("/check")
async def check_favorite(news_id: int=Query(...,alias="news_id"),user:User=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # 检查用户是否收藏了该新闻
    is_favorite = await is_new_favorite(db, user.id, news_id)
    return success_response(
        message="检查收藏状态成功",
        data=FavoriteCheckRequest(isFavorite=is_favorite)
    )

@router.post("/add")
async def add_favorite(data:FavoriteAddRequest,user:User=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
   result = await add_new_favorite(db, user.id, data.news_id)
   return success_response(
        message="收藏新闻成功",
        data=result
    )

@router.delete("/remove")
async def remove_favorite(data:FavoriteAddRequest,user:User=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
   result = await remove_new_favorite(db, user.id, data.news_id)
   if not result:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="收藏记录不存在")
   return success_response(
        message="取消收藏新闻成功",
        data=result
    )

@router.get("/list")
async def get_favorite_lists(page: int = Query(1, ge=1, alias="page"),
                            page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
                            user:User=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rows,total = await get_favorite_list(db, user.id, page, page_size)
    #将 news 对象转换为字典，并添加两个额外字段：favorite_time 和 favorite_id
    favorite_list = [{
        **news.__dict__,
        'favorite_time':favorite_time,
        'favorite_id':favorite_id
    } for news,favorite_time,favorite_id in rows]
    has_more = total > page * page_size
    data = FavoriteListResponse(
        List=favorite_list,
        total=total,
        has_more=has_more
    )
    return success_response(
        message="获取收藏列表成功",
        data=data
    )

@router.delete("/clear")
async def clear_favorite(user:User=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # 清空用户收藏
    count = await clear_favorites(db, user.id)
    return success_response(
        message="清空收藏列表成功",
        data={"count": count}
    )
    
    
