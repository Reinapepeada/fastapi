from fastapi import APIRouter, Header
from typing import Annotated, List
from fastapi import Query
from database.connection.SQLConection import SessionDep
from database.models.product import Product


router = APIRouter()

@router.get("/")
def read_root():
    return {"msg": "Welcome to team celular product's API!"}

@router.get("/product")
def get_product():
    return {"product": "product"}