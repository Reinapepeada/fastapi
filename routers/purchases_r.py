from fastapi import APIRouter
from controllers.purchase_c import create_purchase, delete_purchase, get_purchase_by_id, get_purchases_all, update_purchase
from database.models.purchase import (
    CreatePurchase, 
    UpdatePurchase, 
    PurchaseResponse,
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
    session: SessionDep = SessionDep
)-> PurchaseResponse:
    return create_purchase(purchase=purchase, session=session)

@router.put("/update")
def update_purchase_endp(
    purchase_id: int, 
    purchase: UpdatePurchase, 
    session: SessionDep = SessionDep
)-> PurchaseResponse:
    return update_purchase(purchase=purchase, session=session, purchase_id=purchase_id)

@router.delete("/delete{purchase_id}")
def delete_purchase_endp(
    purchase_id: int,
    session: SessionDep = SessionDep
):
    return delete_purchase(purchase_id=purchase_id, session=session)

@router.get("/get{purchase_id}")
def get_purchase_by_id_endp(
    purchase_id: int,
    session: SessionDep = SessionDep
)-> PurchaseResponse:
    return get_purchase_by_id(purchase_id, session)

@router.get("/get/all")
def get_purchases_all_endp(
    session: SessionDep = SessionDep
)-> List[PurchaseResponse]:
    return get_purchases_all(session)



    
    