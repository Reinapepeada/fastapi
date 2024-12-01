from fastapi import APIRouter, Header
from typing import Annotated, List
from fastapi import Query
from database.connection.SQLConection import SessionDep
from database.models.product import Product


router = APIRouter()

router.get("/hughjgjkh")
def get_products():
    return {"hola": "hola"}