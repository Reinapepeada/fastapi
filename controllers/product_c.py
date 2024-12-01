
from fastapi import HTTPException
from sqlmodel import Session
from database.models.product import CategoryCreate, ProductCreate, ProviderCreate
from services.product_s import create_category_db, create_product_and_variants, create_provider_db, get_category_all, get_provider_all
from services import auth_s

def create_product(product: ProductCreate, session: Session):
    try:
        create_product_and_variants(product, session)
        return {"msg": "Product created successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
def create_category(category: CategoryCreate, session: Session):
    try:
        create_category_db(category, session)
        return {"msg": "Category created successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def get_category(session: Session):
    try:
        return get_category_all(session)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def create_provider(provider: ProviderCreate, session: Session):
    try:
        create_provider_db(provider, session)
        return {"msg": "Provider created successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def get_provider(session: Session):
    try:
        return get_provider_all(session)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    