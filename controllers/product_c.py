
from fastapi import HTTPException
from sqlmodel import Session
from database.models.product import BranchCreate, BrandCreate, CategoryCreate, ProductCreate, ProductUpdate, ProductVariantUpdate, ProviderCreate
from services.branch_s import create_branch_db, delete_branch_db, get_branches_all, update_branch_db
from services.brand_s import create_brand_db, delete_brand_db, get_brands_all, update_brand_db
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
        product_variants=create_product_and_variants(product, session)
        return product_variants
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
def update_product(product_id: int, product: ProductUpdate, session: Session):
    try:
        product_variants=update_product_db(product_id, product, session)
        return product_variants
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def update_product_variant(variant_id: int, variant: ProductVariantUpdate, session: Session):
    try:
        product_variants=update_product_variant_db(variant_id, variant, session)
        return product_variants
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
        category=create_category_db(category, session)
        return category
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def get_categories_all(session: Session):
    try:
        return get_categories_all_db(session)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def create_provider(provider: ProviderCreate, session: Session):
    try:
        provider=create_provider_db(provider, session)
        return provider
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
        branch=create_branch_db(branch, session)
        return branch
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
        branch=update_branch_db(branch_id, branch, session)
        return branch
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
#  brand controller
def create_brand(brand: BrandCreate, session: Session):
    try:
        brand=create_brand_db(brand, session)
        return brand
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def get_brands(session: Session):
    try:
        return get_brands_all(session)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def delete_brand(brand_id: int, session: Session):
    try:
        delete_brand_db(brand_id, session)
        return {"msg": "Brand deleted successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def update_brand(brand_id: int, brand: BrandCreate, session: Session):
    try:
        brand=update_brand_db(brand_id, brand, session)
        return brand
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))