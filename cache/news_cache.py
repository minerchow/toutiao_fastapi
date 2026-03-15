#新闻相关缓存方法
CATEGORY_KEY = "news:categories"
NEWS_LIST_KEY = "news:list"
from config.cache_config import get_json_cache, set_cache
from typing import List, Dict, Any, Optional


#获取新闻缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORY_KEY)


#写入新闻
# 列表600 配置7200 List[Dict[str,Any]等价于ts的data: Array<{ [key: string]: any }>
'''
data: Array<{ 
  id: number;
  name: string;
  sort_order: number;
}>
'''
async def set_cached_categories(data:List[Dict[str,Any]],expire: int = 7200):
    await set_cache(CATEGORY_KEY, data, expire)


# 写入缓存新闻列表 key=name_list::分类id::页码:每页数量
async def set_cached_categories_list(category_id: Optional[int], page: int, page_size: int, data:List[Dict[str,Any]],expire: int = 600):
    # 调用 封装的 Redis 的设置方法，存新闻列表到缓存
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_KEY}{category_part}:{page}:{page_size}"
    return await set_cache(key, data, expire)
# 读取缓存新闻列表
async def get_cache_news_list(category_id: Optional[int], page: int, page_size: int):
     category_part = category_id if category_id is not None else "all"
     key = f"{NEWS_LIST_KEY}{category_part}:{page}:{page_size}"
     return await get_json_cache(key)
