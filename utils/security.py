from passlib.context import CryptContext

#密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#密码加密
def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)