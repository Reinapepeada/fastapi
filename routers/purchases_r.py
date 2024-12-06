from fastapi import APIRouter, Header
from controllers.purchase_c import create_purchase, create_purchase_item, delete_purchase, delete_purchase_item, get_purchase_by_id, get_purchases_all, update_purchase, update_purchase_item
from database.models.purchase import (
    CreatePurchase, 
    CreatePurchaseItem, 
    UpdatePurchase, 
    UpdatePurchaseItem,
    PurchaseResponse,
    PurchaseItemResponse
    )
from database.connection.SQLConection import SessionDep
from typing import List

router = APIRouter()


@router.get("/")
def main_purchase():
    return {"msg": "welcome to purchases"}

@router.post("/create")
def create_purchase_endp(
    purchase: CreatePurchase,
    session: SessionDep
)-> PurchaseResponse:
    return create_purchase(purchase, session)

@router.put("/update")
def update_purchase_endp(
    purchase_id: int, 
    purchase: UpdatePurchase, 
    session: SessionDep
)-> PurchaseResponse:
    return update_purchase(purchase_id, purchase, session)

@router.delete("/delete{purchase_id}")
def delete_purchase_endp(
    purchase_id: int,
    session: SessionDep
):
    return delete_purchase(purchase_id, session)

@router.get("/get{purchase_id}")
def get_purchase_by_id_endp(
    purchase_id: int,
    session: SessionDep
)-> PurchaseResponse:
    return get_purchase_by_id(purchase_id, session)

@router.get("/get/all")
def get_purchases_all_endp(
    session: SessionDep
)-> List[PurchaseResponse]:
    return get_purchases_all(session)

@router.post("/create/item")
def create_purchase_item_endp(
    item: CreatePurchaseItem,
    session: SessionDep
)-> PurchaseItemResponse:
    return create_purchase_item(item, session)

@router.put("/update/item{item_id}")
def update_purchase_item_endp(
    item_id: int,
    item: UpdatePurchaseItem,
    session: SessionDep
)-> PurchaseItemResponse:
    return update_purchase_item(item_id, item, session)

@router.delete("/delete/item{item_id}")
def delete_purchase_item_endp(
    item_id: int,
    session: SessionDep
):
    return delete_purchase_item(item_id, session)



    
    