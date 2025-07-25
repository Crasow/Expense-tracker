from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..dependencies import get_db, get_current_user
from ..schemas.balance_change import (
    BalanceChangeRead,
    BalanceChangeCreate,
    BalanceChangeUpdate,
)
from ..crud.balance_change import (
    get_balance_changes,
    create_balance_change,
    update_balance_change,
    get_balance_change,
    delete_balance_change,
)


router = APIRouter(prefix="/balance_change", tags=["balance_change"])


@router.get("/", response_model=List[BalanceChangeRead])
def get_balance_changes_by_user_id(
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return get_balance_changes(db, user.id)


@router.get("/{balance_change_id}", response_model=BalanceChangeRead)
def get_balance_change_by_id(
    balance_change_id: int,
    db: Session = Depends(get_db),
):
    balance_change = get_balance_change(db, balance_change_id)
    if not balance_change:
        raise HTTPException(status_code=404, detail="Balance change not found")
    return balance_change


@router.post("/", response_model=BalanceChangeRead)
def create_new_balance_change(
    balance_change: BalanceChangeCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return create_balance_change(db, balance_change)


@router.put("/{balance_change_id}", response_model=BalanceChangeRead)
def update_balance_change_by_id(
    balance_change_id: int,
    balance_change: BalanceChangeUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return update_balance_change(db, balance_change_id, balance_change)


@router.delete("/{balance_change_id}", status_code=204)
def delete_balance_change(
    balance_change_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    delete_balance_change(db, balance_change_id)