from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from expense_tracker.models.user import User
from expense_tracker.schemas.user import UserCreate

async def create_user(db:AsyncSession, user: UserCreate) -> User:
    db_user = User(username = user.username, email = user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_username(db:AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()