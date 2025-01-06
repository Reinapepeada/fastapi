
from fastapi import HTTPException
from sqlmodel import Session
# modelos de las tablas
from database.models.product import BranchCreate, BrandCreate, CategoryCreate, ProductCreate, ProductUpdate, ProductVariantCreateList, ProductVariantUpdate, ProviderCreate

from services.product_s import (
    create_product_db,
    create_product_variant_db,
    delete_product_db,
    delete_product_variant_db,
    get_product_by_id_db,
    get_product_variants_by_product_id_db,
    get_products_all_db,
    update_product_db,
    update_product_variant_db
    )

# Crud operations for auxiliary tables
from services.branch_s import create_branch_db, delete_branch_db, get_branches_all, update_branch_db
from services.brand_s import create_brand_db, delete_brand_db, get_brands_all, update_brand_db
from services.providers_s import create_provider_db, delete_provider_db, get_providers_all, update_provider_db
from services.category_s import delete_category_db, get_categories_all_db, update_category_db, create_category_db


def create_product(product: ProductCreate, session: Session):
    try:
        return create_product_db(product, session)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def get_products_all(session: Session):
    try:
        return get_products_all_db(session)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


from services.product_s import fetch_products_with_pagination


async def get_paginated_products_controller(
    session: Session, page: int, size: int
):
    products, total_count = await fetch_products_with_pagination(session, page, size)
    return {
        "products": products,
        "total": total_count,
        "page": page,
        "size": size,
        "pages": (total_count + size - 1) // size,  # Calculate total pages
    }

def get_products_by_id(product_id: int, session: Session):
    try:
        return get_product_by_id_db(session, product_id)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
def update_product(product_id: int, product: ProductUpdate, session: Session):
    try:
        product_variants=update_product_db(product_id, product, session)
        return product_variants
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def delete_product(product_id: int, session: Session):
    try:
        return delete_product_db(product_id, session)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
def create_product_variant(variant: ProductVariantCreateList, session: Session):
    try:
        return create_product_variant_db(variant, session)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def get_product_variants_by_product_id(product_id: int, session: Session):
    try:
        return get_product_variants_by_product_id_db(product_id, session)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def update_product_variant(variant_id: int, variant: ProductVariantUpdate, session: Session):
    try:
        product_variants=update_product_variant_db(variant_id, variant, session)
        return product_variants
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def delete_product_variant(variant_id: int, session: Session):
    try:
        return delete_product_variant_db(variant_id, session) 
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

# provider controller
def create_provider(provider: ProviderCreate, session: Session):
    try:
        provider=create_provider_db(provider, session)
        return provider
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def get_providers(session: Session):
    try:
        return get_providers_all(session)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def delete_provider(provider_id: int, session: Session):
    try:
        delete_provider_db(provider_id, session)
        return {"msg": "provider deleted successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def update_provider(provider_id: int, provider: ProviderCreate, session: Session):
    try:
        provider=update_provider_db(provider_id, provider, session)
        return provider
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

# category controller

def create_category(category: CategoryCreate, session: Session):
    try:
        category=create_category_db(category, session)
        return category
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def get_categories(session: Session):
    try:
        return get_categories_all_db(session)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def delete_category(category_id: int, session: Session):
    try:
        delete_category_db(category_id, session)
        return {"msg": "category deleted successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def update_category(category_id: int, category: CategoryCreate, session: Session):
    try:
        category=update_category_db(category_id, category, session)
        return category
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))