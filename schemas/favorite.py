from pydantic import BaseModel, Field,ConfigDict
from schemas.base import NewsItemBase
from datetime import datetime
class FavoriteCheckRequest(BaseModel):
   is_favorite: bool = Field(..., alias="isFavorite", description="是否收藏")

class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", description="新闻ID")

# 新闻模型 + 收藏模型
class FavoriteNewsItem(NewsItemBase):
    favorite_id: int = Field(..., alias="favoriteId", description="收藏ID")
    favorite_time: datetime = Field(..., alias="favoriteTime", description="收藏时间")
    model_config = ConfigDict(from_attributes=True,populate_by_name=True)

# 收藏列表响应
class FavoriteListResponse(BaseModel):
    List: list[FavoriteNewsItem]
    total: int = Field(..., description="总收藏数")
    has_more: bool = Field(..., alias="hasMore", description="是否还有更多")
    model_config = ConfigDict(from_attributes=True,populate_by_name=True)
   