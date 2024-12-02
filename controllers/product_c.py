
from fastapi import HTTPException
from sqlmodel import Session
from database.models.product import BranchCreate, CategoryCreate, ProductCreate, ProductUpdate, ProductVariantUpdate, ProviderCreate
from services.branch_s import create_branch_db, delete_branch_db, get_branches_all, update_branch_db
from services.product_s import (
    create_category_db, 
    create_product_and_variants, 
    create_provider_db,
    delete_product_db,
    delete_product_variant_db,
    get_categories_all_db, 
    get_provider_all,
    update_product_db,
    update_product_variant_db
    )
from services import auth_s

def create_product(product: ProductCreate, session: Session):
    try:
        create_product_and_variants(product, session)
        return {"msg": "Product created successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
def update_product(product_id: int, product: ProductUpdate, session: Session):
    try:
        update_product_db(product_id, product, session)
        return {"msg": "Product updated successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def update_product_variant(variant_id: int, variant: ProductVariantUpdate, session: Session):
    try:
        update_product_variant_db(variant_id, variant, session)
        return {"msg": "Product variant updated successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def delete_product(product_id: int, session: Session):
    try:
        delete_product_db(product_id, session)
        return {"msg": "Product deleted successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def delete_product_variant(variant_id: int, session: Session):
    try:
        delete_product_variant_db(variant_id, session)
        return {"msg": "Product variant deleted successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
def create_category(category: CategoryCreate, session: Session):
    try:
        create_category_db(category, session)
        return {"msg": "Category created successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def get_categories_all(session: Session):
    try:
        return get_categories_all_db(session)
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
    

# branches controller
def create_branch(branch: BranchCreate, session: Session):
    try:
        create_branch_db(branch, session)
        return {"msg": "Branch created successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def get_branches(session: Session):
    try:
        return get_branches_all(session)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def delete_branch(branch_id: int, session: Session):
    try:
        delete_branch_db(branch_id, session)
        return {"msg": "Branch deleted successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def update_branch(branch_id: int, branch: BranchCreate, session: Session):
    try:
        update_branch_db(branch_id, branch, session)
        return {"msg": "Branch updated successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
    