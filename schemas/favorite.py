from pydantic import BaseModel, Field,ConfigDict

class FavoriteCheckRequest(BaseModel):
   is_favorite: bool = Field(..., alias="isFavorite", description="是否收藏")

class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", description="新闻ID")
