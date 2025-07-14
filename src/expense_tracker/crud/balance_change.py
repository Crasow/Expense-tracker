from sqlalchemy.ext.asyncio import AsyncSession
from expense_tracker.models.balance_change import BalanceChange
from expense_tracker.schemas.balance_change import (
    BalanceChangeBase,
    BalanceChangeCreate,
    BalanceChangeRead,
    BalanceChangeUpdate,
)
from expense_tracker.crud.category import get_category_by_id
from sqlalchemy import select
from fastapi import HTTPException
from typing import List


async def create_balance_change(
    db: AsyncSession, balance_change_data: BalanceChangeCreate
) -> BalanceChange:
    balance_change = BalanceChange(**balance_change_data.model_dump())
    db.add(balance_change)
    await db.commit()
    await db.refresh(balance_change)
    return balance_change


async def get_balance_change_by_id(
    db: AsyncSession, balance_change_id: int
) -> BalanceChange:
    result = await db.execute(
        select(BalanceChange).where(BalanceChange.id == balance_change_id)
    )
    return result.scalar_one_or_none()


async def get_balance_changes_by_user_id(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10
) -> List[BalanceChange]:
    result = await db.execute(
        select(BalanceChange)
        .where(BalanceChange.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def update_balance_change(
    db: AsyncSession, balance_change_id: int, balance_change_data: BalanceChangeUpdate
) -> BalanceChange:
    balance_change = await get_balance_change_by_id(db, balance_change_id)
    if not balance_change:
        raise HTTPException(status_code=404, detail="Balance change not found")

    for field, value in balance_change_data.model_dump(exclude_unset=True).items():
        if field == "category_id":
            category = await get_category_by_id(db, value)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            balance_change.category = category
        else:
            setattr(balance_change, field, value)

    db.add(balance_change)
    await db.commit()
    await db.refresh(balance_change)
    return balance_change


async def delete_balance_change(db: AsyncSession, balance_change_id: int) -> None:
    balance_change = await get_balance_change_by_id(db, balance_change_id)
    if not balance_change:
        raise HTTPException(status_code=404, detail="Balance change not found")
    await db.delete(balance_change)
