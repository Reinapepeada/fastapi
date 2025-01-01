from fastapi import APIRouter
from typing import List
from controllers.product_c import create_brand, delete_brand, get_brands, update_brand
from database.connection.SQLConection import SessionDep

from database.models.product import (
    BrandCreate,
    BrandOut)
# enpoints for brandes
router = APIRouter()

@router.post("/create")
def create_brand_endp(
    brand: BrandCreate,
    session: SessionDep = SessionDep
):
    return create_brand(brand, session)

@router.get("/get/all")
def get_brand_endp(
    session: SessionDep = SessionDep
)-> List[BrandOut]:
    return get_brands(session)

@router.delete("/delete")
def delete_brand_endp(
    brand_id: int,
    session: SessionDep = SessionDep
):
    return delete_brand(brand_id, session)

@router.put("/update")
def update_brand_endp(
    brand_id: int,
    brand: BrandCreate,
    session: SessionDep = SessionDep
):
    return update_brand(brand_id, brand, session)