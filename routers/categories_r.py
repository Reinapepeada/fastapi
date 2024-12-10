from fastapi import APIRouter
from typing import List
from controllers.product_c import create_category, delete_category, get_categories, update_category
from database.connection.SQLConection import SessionDep

from database.models.product import (
    CategoryCreate,
    CategoryOut)
# enpoints for categoryes
router = APIRouter()

@router.post("/create")
def create_category_endp(
    category: CategoryCreate,
    session: SessionDep = SessionDep
)-> CategoryOut:
    return create_category(category, session)

@router.get("/get/all")
def get_category_endp(
    session: SessionDep = SessionDep
)-> List[CategoryOut]:
    return get_categories(session)

@router.delete("/delete")
def delete_category_endp(
    category_id: int,
    session: SessionDep = SessionDep
):
    return delete_category(category_id, session)

@router.put("/update")
def update_category_endp(
    category_id: int,
    category: CategoryCreate,
    session: SessionDep = SessionDep
)-> CategoryOut:
    return update_category(category_id, category, session)