from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.schemas.user import UserCreate, UserRead
from expense_tracker.crud.user import create_user, get_user_by_username
from expense_tracker.dependencies import get_db, get_current_user
from expense_tracker.utils.auth import create_access_token
from expense_tracker.schemas.user import Token, UserLogin
from expense_tracker.crud.user import verify_password, get_users

router = APIRouter()


@router.post("/users", response_model=UserRead)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    return await create_user(db, user)


@router.get("/me")
async def read_me(current_user: str = Depends(get_current_user)):
    return {"user": current_user}


@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_username(db, user.username)

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token({"sub": db_user.username})

    return {"access_token": token, "token_type": "bearer"}


@router.post("/joke_login", response_model=Token)
async def joke_login(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_username(db, user_login.username)

    if not db_user or not verify_password(user_login.password, db_user.hashed_password):
        users = await get_users(db)
        for user in users:
            if verify_password(user_login.password, user.hashed_password):
                raise HTTPException(
                    status_code=400,
                    detail=f"This is a wrong password for this user.User \"{user.username}\" has this password! It`s u?",
                )

    token = create_access_token({"sub": db_user.username})

    return {"access_token": token, "token_type": "bearer"}
