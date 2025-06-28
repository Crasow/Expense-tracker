from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: UUID
