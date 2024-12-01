from fastapi import APIRouter, Header
from typing import Annotated, List
from fastapi import Query
from database.connection.SQLConection import SessionDep
from database.models.product import (
    CategoryCreate,
    CategoryOut, 
    ProductCreate, 
    ProductUpdate, 
    ProductOut, 
    ProductVariantCreate, 
    ProductVariantOut, 
    ProductVariantUpdate,
    ProviderCreate, 
    ProviderOut,
    ProviderUpdate 
    )
from controllers.product_c import create_category, create_product, create_provider, get_category, get_provider

router = APIRouter()

@router.get("/")
def read_root():
    return {"msg": "Welcome to team celular product's API!"}

@router.post("/create")
def create_product_endp(
    product: ProductCreate,
    session: SessionDep = SessionDep
):
    print(product)
    return create_product(product, session)

@router.post("/create/category")
def create_category_endp(
    category: CategoryCreate,
    session: SessionDep = SessionDep
):
    return create_category(category, session)

@router.get("/get/category")
def get_category_endp(
    session: SessionDep = SessionDep
)-> List[CategoryOut]:
    return get_category(session)

@router.post("/create/provider")
def create_provider_endp(
    provider: ProviderCreate,
    session: SessionDep = SessionDep
):
    return create_provider(provider, session)

@router.get("/get/provider")
def get_provider_endp(
    session: SessionDep = SessionDep
)-> List[ProviderOut]:
    return get_provider(session)
