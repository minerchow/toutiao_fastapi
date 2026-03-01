from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from schemas.users import UserAuthResponse, UserInfoResponse, UserRequest
from crud.users import get_user_by_username, create_user, create_token
from utils.response import success_response

router = APIRouter(prefix="/api/users",tags=["users"])

@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession = Depends(get_db)):
    # 检查用户名是否已存在
    existing_user = await get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    # 新增用户
    new_user = await create_user(db, user_data)
    # 生成token
    token = await create_token(db, new_user)
    response_data = UserAuthResponse(token=token,userInfo=UserInfoResponse.model_validate(new_user));
    return success_response(
        message="注册成功",
        data=response_data
    )