from fastapi import APIRouter, Header
from typing import Annotated, List
from fastapi import Query
from database.connection.SQLConection import SessionDep
from database.models.product import (
    BranchCreate,
    BranchOut,
    CategoryCreate,
    CategoryOut, 
    ProductCreate, 
    ProductUpdate, 
    ProductOut, 
    ProductVariantOut, 
    ProductVariantUpdate,
    ProviderCreate, 
    ProviderOut,
    ProviderUpdate 
    )
from controllers.product_c import create_category, create_product, create_provider, delete_branch, delete_product, delete_product_variant, get_branches, get_categories_all, get_provider, update_branch, update_product, update_product_variant


router = APIRouter()

@router.get("/")
def read_root():
    return {"msg": "Welcome to team celular product's API!"}

@router.post("/create")
def create_product_and_variants_endp(
    product: ProductCreate,
    session: SessionDep = SessionDep
) -> ProductOut:
    print(product)
    return create_product(product, session)

@router.put("/update")
def update_product_endp(
    product_id: int,
    product: ProductUpdate,
    session: SessionDep = SessionDep
)-> ProductOut:
    return update_product(product_id, product, session)

@router.put("/update/variant")
def update_product_variant_endp(
    variant_id: int,
    variant: ProductVariantUpdate,
    session: SessionDep = SessionDep
)-> ProductVariantOut:
    return update_product_variant(variant_id, variant, session)

@router.delete("/delete")
def delete_product_endp(
    product_id: int,
    session: SessionDep = SessionDep
):
    return delete_product(product_id, session)

@router.delete("/delete/variant")
def delete_product_variant_endp(
    variant_id: int,
    session: SessionDep = SessionDep
):
    return delete_product_variant(variant_id, session)


@router.post("/create/category")
def create_category_endp(
    category: CategoryCreate,
    session: SessionDep = SessionDep
)-> CategoryOut:
    return create_category(category, session)

@router.get("/get/category")
def get_category_endp(
    session: SessionDep = SessionDep
)-> List[CategoryOut]:
    return get_categories_all(session)

@router.post("/create/provider")
def create_provider_endp(
    provider: ProviderCreate,
    session: SessionDep = SessionDep
)-> ProviderOut:
    return create_provider(provider, session)

@router.get("/get/provider")
def get_provider_endp(
    session: SessionDep = SessionDep
)-> List[ProviderOut]:
    return get_provider(session)

# enpoints for branches

@router.post("/create/branch")
def create_branch_endp(
    branch: BranchCreate,
    session: SessionDep = SessionDep
)-> BranchOut:
    return create_branch(branch, session)

@router.get("/get/branch")
def get_branch_endp(
    session: SessionDep = SessionDep
)-> List[BranchOut]:
    return get_branches(session)

@router.delete("/delete/branch")
def delete_branch_endp(
    branch_id: int,
    session: SessionDep = SessionDep
):
    return delete_branch(branch_id, session)

@router.put("/update/branch")
def update_branch_endp(
    branch_id: int,
    branch: BranchCreate,
    session: SessionDep = SessionDep
):
    return update_branch(branch_id, branch, session)