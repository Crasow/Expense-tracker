from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from ..crud.category import (
    create_category,
    get_categories,
    get_category,
    update_category,
    delete_category,
)
from ..dependencies import get_db, get_current_user
from typing import List

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryRead])
def get_categories_by_user_id(
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return get_categories(db, user.id)


@router.get("/{category_id}", response_model=CategoryRead)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryRead)
def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return create_category(db, category, user.id)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category_by_id(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return update_category(db, category_id, category)


@router.delete("/{category_id}", status_code=204)
def delete_category_by_id(
    category_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    delete_category(db, category_id)
