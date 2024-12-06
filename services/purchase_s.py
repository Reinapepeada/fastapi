from fastapi import HTTPException
from sqlmodel import select
from database.models.purchase import (
    CreatePurchase,
    CreatePurchaseItem,
    Purchase, 
    PurchaseItem,
    UpdatePurchase,
    UpdatePurchaseItem
)
from services.product_s import add_stock_product_variant, ensure_product_exists_id, ensure_product_variant_exists, reduce_stock_product_variant
from services.providers_s import ensure_provider_exists




def ensure_purchase_exists(purchase_id: int, session):
    purchase = session.exec(select(Purchase).where(Purchase.id == purchase_id)).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase

def ensure_purchase_item_exists(item_id: int, session):
    item = session.exec(select(PurchaseItem).where(PurchaseItem.id == item_id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

def create_purchase_db(session, purchase) :
    try:
        items = purchase.items
        total_price = 0
        ensure_provider_exists(purchase.provider_id, session)
        for item in items:
            total_price += item.cost * item.quantity

        db_purchase = Purchase(
            provider_id=purchase.provider_id,
            total_price=total_price
        )
        session.add(db_purchase)
        session.commit()
        session.refresh(db_purchase)
        for item in items:
            total_cost = item.cost * item.quantity
            ensure_product_variant_exists(item.productvariant_id, session)
            ensure_product_exists_id(item.product_id, session)
            purchase_item = PurchaseItem(
                product_id=item.product_id,
                productvariant_id=item.productvariant_id,
                quantity=item.quantity,
                cost=item.cost,
                total_cost=total_cost,
                purchase_id=db_purchase.id
            )
            session.add(purchase_item)
            session.commit()
            session.refresh(purchase_item)
            add_stock_product_variant(session=session,variant_id= item.productvariant_id,quantity=item.quantity)
        return db_purchase
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating purchase: {str(e)}")

def update_purchase_db(session, purchase: UpdatePurchase, purchase_id):
    try:
        db_purchase = ensure_purchase_exists(purchase_id, session)
        if not db_purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")
        if purchase.provider_id :
            db_purchase.provider_id = purchase.provider_id
        if purchase.items:
            purchase_total_price = 0
            for item in purchase.items:
                db_item = ensure_purchase_item_exists(item.id, session)
                # update stock in variant
                if item.quantity > db_item.quantity:
                    add_stock_product_variant(session=session, variant_id=db_item.productvariant_id, quantity=(item.quantity - db_item.quantity))
                else :
                    reduce_stock_product_variant(session=session, variant_id=db_item.productvariant_id, quantity=(db_item.quantity - item.quantity))
                # update item
                for key, value in item.model_dump(exclude_unset=True).items():
                    setattr(db_item, key, value)                
                # update total cost
                db_item.total_cost = db_item.cost * db_item.quantity
                purchase_total_price += db_item.total_cost
            db_purchase.total_price = purchase_total_price
        session.commit()
        session.refresh(db_purchase)
        return db_purchase
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating purchase: {str(e)}")
    
def delete_purchase_db(session, purchase_id):
    try:
        db_purchase = ensure_purchase_exists(purchase_id, session)
        # reduce stock
        for item in db_purchase.items:
            reduce_stock_product_variant(session=session,variant_id= item.productvariant_id,quantity=item.quantity)
        session.delete(db_purchase)
        session.commit()
        return {"msg": "Purchase deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting purchase: {str(e)}")

    
def get_purchase_by_id_db(session, purchase_id):
    try:
        db_purchase = ensure_purchase_exists(purchase_id, session)
        return db_purchase
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error getting purchase: {str(e)}")
    
def get_purchases_all_db(session):
    try:
        purchases = session.exec(select(Purchase)).all()
        return purchases
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error getting purchases: {str(e)}")

# purchase item services

def create_purchase_item_db(session, item: CreatePurchaseItem):
    try:
        total_cost = item.cost * item.quantity
        db_item = PurchaseItem(
            product_id=item.product_id,
            productvariant_id=item.productvariant_id,
            purchase_id=item.purchase_id,
            quantity=item.quantity,
            cost=item.cost,
            total_cost=total_cost
        )
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating item: {str(e)}")

def update_purchase_item_db(session, item_id, item: UpdatePurchaseItem):
    try:
        db_item = ensure_purchase_item_exists(item_id, session)
        for key, value in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)
        session.commit()
        session.refresh(db_item)
        return db_item
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating item: {str(e)}")

def delete_purchase_item_db(session, item_id):
    try:
        db_item = ensure_purchase_item_exists(item_id, session)
        session.delete(db_item)
        session.commit()
        return {"msg": "Item deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting item: {str(e)}")
