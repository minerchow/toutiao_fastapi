
from datetime import datetime, timedelta
from uuid import uuid4
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest, UserChangePasswordRequest
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


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user

# 通过token查询用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalars().one_or_none()
    if not db_token:
        return None
    if db_token.expires_at < datetime.now():
        return None
    query = select(User).where(User.id == db_token.user_id) 
    result = await db.execute(query)
    return result.scalars().one_or_none()


 # 更新用户信息
async def update_user_info(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    # user_data 转换为字典，排除未设置的字段 没有设置的字段不更新
    query = update(User).where(User.username == username).values(**user_data.model_dump(exclude_unset=True,
    exclude_none=True))
    result = await db.execute(query)
    await db.commit()
    # 检查更新是否成功
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="用户不存在")
   # 获取更新后的用户信息
    updated_user = await get_user_by_username(db, username)
    return updated_user

# 修改密码 验证旧密码  新密码加密 修改密码
async def update_user_password(db: AsyncSession, user:User, password_data: UserChangePasswordRequest):
    # 验证旧密码
    if not security.verify_password(password_data.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="旧密码错误")
    # 更新密码
    user.password = security.get_hash_password(password_data.new_password)
    db.add(user);
    await db.commit()
    await db.refresh(user)
    return True
        
