from sqlalchemy.ext.asyncio import AsyncSession
from expense_tracker.db import async_session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from expense_tracker.utils.auth import decode_access_token


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username
