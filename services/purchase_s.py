from fastapi import HTTPException
from database.models.purchase import (
    CreatePurchase,
    CreatePurchaseItem,
    Purchase, 
    PurchaseItem,
    UpdatePurchase,
    UpdatePurchaseItem
)
from services.product_s import add_stock_product_variant, reduce_stock_product_variant




def ensure_purchase_exists(purchase_id: int, session):
    purchase = session.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase

def ensure_purchase_item_exists(item_id: int, session):
    item = session.query(PurchaseItem).filter(PurchaseItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item



def create_purchase_db(session , purchase: CreatePurchase) -> Purchase:
    try:
        items = purchase.items
        total_price = 0
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
            add_stock_product_variant(session, item.productvariant_id, item.quantity)
        return db_purchase
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating purchase: {str(e)}")

def update_purchase_db(session, purchase:UpdatePurchase, purchase_id):
    try:
        db_purchase = ensure_purchase_exists(purchase_id, session)
        if not db_purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")
        for key, value in purchase.model_dump(exclude_unset=True).items():
            setattr(db_purchase, key, value)
        if purchase.items:
            for item in purchase.items:
                db_item = ensure_purchase_item_exists(item.id, session)
                for key, value in item.model_dump(exclude_unset=True).items():
                    setattr(db_item, key, value)                
                # update stock
                if item.quantity > db_item.quantity:
                    add_stock_product_variant(session, db_item.productvariant_id, item.quantity - db_item.quantity)
                elif item.quantity < db_item.quantity:
                    reduce_stock_product_variant(session, db_item.productvariant_id, db_item.quantity - item.quantity)

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
            reduce_stock_product_variant(session, item.productvariant_id, item.quantity)
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
        purchases = session.query(Purchase).all()
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
