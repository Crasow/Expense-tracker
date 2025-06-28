from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.schemas.user import UserCreate, UserRead
from expense_tracker.crud.user import create_user, get_user_by_username
from expense_tracker.dependencies import get_db 

router = APIRouter()


@router.post("/users", response_model=UserRead)
async def register_user(user:UserCreate, db:AsyncSession = Depends(get_db)):
    existing = await get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    return await create_user(db, user)