
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import User, UserToken
from schemas.users import UserRequest
from utils import security

#根据用户名查询用户
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalars().one_or_none()

#创建用户 先加密密码
async def create_user(db: AsyncSession, user_data: UserRequest):
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user) #刷新数据库中的用户对象，确保返回的用户对象是最新的
    return user

#生成token
async def create_token(db: AsyncSession, user: User):
    token = str(uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user.id)
    result = await db.execute(query)
    user_token = result.scalars().one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user.id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    return token 