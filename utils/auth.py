#整合 token查询用户
from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import UserToken
from utils import security
from config.db_conf  import get_db
from crud.users import get_user_by_token
async def get_current_user(authorization: str = Header(default=None), db: AsyncSession = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    parts = authorization.split(" ")
    token = parts[1] if len(parts) > 1 else parts[0]
    user = await get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
