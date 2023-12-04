from pytz import timezone

from typing import Optional, List

from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.user_model import UserModel
from core.configs import settings
from core.security import verify_password

from pydantic import EmailStr


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usarios/login"
)

async def authenticate(email: EmailStr, passwd: str, db: AsyncSession) -> Optional[UserModel]:
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        user: UserModel =  result.scalars().unique().one_or_none()
        
        if not user:
            return None
        
        if not verify_password(passwd, user.senha):
            return None
        
        return user
    
def _create_token(type_token: str, life_time: timedelta, subject: str) -> str:
    #https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    payload = {}
    
    sp = timezone('America/Sao_Paulo')
    expiration = datetime.now(tz=sp) + life_time
    
    payload["type"] = type_token
    
    payload["exp"] = expiration
    
    payload["iat"] = datetime.now(tz=sp)
    
    payload["sub"] = str(subject)
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def create_access_token(subject: str) -> str:
    # https://jwt.io
    return _create_token(life_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                         subject=subject,
                         type_token='access_token')