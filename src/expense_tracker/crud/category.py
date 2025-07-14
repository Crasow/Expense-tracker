from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from expense_tracker.models.category import Category
from expense_tracker.schemas.category import (
    CategoryBase,
    CategoryResponse,
    CategoryUpdate,
)
from typing import List
from fastapi import HTTPException


async def create_category(
    db: AsyncSession, category_data: CategoryBase, user_id: int
) -> Category:
    category = Category(**category_data, user_id=user_id)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_categories_by_user_id(db: AsyncSession, user_id: int) -> List[Category]:
    result = await db.execute(select(Category).where(Category.user_id == user_id))
    return result.scalars().all()


async def get_category_by_id(db: AsyncSession, category_id: int) -> Category:
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()


async def update_category_by_id(
    db: AsyncSession, category_id: int, category_data: CategoryUpdate
) -> Category:
    category = await get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for field, value in category_data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)

    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category_by_id(db: AsyncSession, category_id: int) -> None:
    category = await get_category_by_id(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.delete(category)
    await db.commit()
