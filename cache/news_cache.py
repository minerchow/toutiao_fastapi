#新闻相关缓存方法
CATEGORY_KEY = "news:categories"
from config.cache_config import get_json_cache, set_cache
from typing import List, Dict, Any

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
