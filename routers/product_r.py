from fastapi import APIRouter, Header
from typing import Annotated, List
from fastapi import Query
from database.connection.SQLConection import SessionDep
from database.models.product import (
    BranchCreate,
    BranchOut,
    BrandCreate,
    BrandOut,
    CategoryCreate,
    CategoryOut,
    CategoryUpdate, 
    ProductCreate, 
    ProductUpdate, 
    ProductOut,
    ProductVariantCreateList, 
    ProductVariantOut, 
    ProductVariantUpdate,
    ProviderCreate, 
    ProviderOut,
    ProviderUpdate 
    )
from controllers.product_c import (
    create_branch,
    create_brand,
    create_category, 
    create_product,
    create_product_variant, 
    create_provider, 
    delete_branch, 
    delete_brand, 
    delete_category, 
    delete_product, delete_product_variant, delete_provider, get_branches, get_brands, get_categories,
    get_product_variants_by_product_id,
    get_products_all, get_providers, update_branch, update_brand, update_category, update_product, update_product_variant, update_provider
)

router = APIRouter()

@router.get("/")
def read_root():
    return {"msg": "Welcome to team celular product's API!"}

# product endpoints

@router.post("/create")
def create_product_endp(
    product: ProductCreate,
    session: SessionDep = SessionDep
)-> ProductOut:
    return create_product(product, session)

@router.get("/get")
def get_products_endp(
    session: SessionDep = SessionDep
)-> List[ProductOut]:
    return get_products_all(session)

@router.put("/update")
def update_product_endp(
    product_id: int,
    product: ProductUpdate,
    session: SessionDep = SessionDep
)-> ProductOut:
    return update_product(product_id, product, session)

@router.delete("/delete")
def delete_product_endp(
    product_id: int,
    session: SessionDep = SessionDep
):
    return delete_product(product_id, session)



# endpoints for product variants
@router.post("/create/variant")
def create_product_variant_endp(
    variant: ProductVariantCreateList,
    session: SessionDep = SessionDep
)-> list[ProductVariantOut]:
    return create_product_variant(variant, session)

@router.get("/get/variant")
def get_product_variants_by_product_id_endp(
    product_id: int,
    session: SessionDep = SessionDep
)-> List[ProductVariantOut]:
    return get_product_variants_by_product_id(product_id, session)

@router.put("/update/variant")
def update_product_variant_endp(
    variant_id: int,
    variant: ProductVariantUpdate,
    session: SessionDep = SessionDep
)-> ProductVariantOut:
    return update_product_variant(variant_id, variant, session)

@router.delete("/delete/variant")
def delete_product_variant_endp(
    variant_id: int,
    session: SessionDep = SessionDep):
    return delete_product_variant(variant_id, session)


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
)-> BranchOut:
    return update_branch(branch_id, branch, session)

# endpoints for brands 

@router.post("/create/brand")
def create_brand_endp(
    brand: BrandCreate,
    session: SessionDep = SessionDep
)-> BrandOut:
    return create_brand(brand, session)

@router.get("/get/brand")
def get_brand_endp(
    session: SessionDep = SessionDep
)-> List[BrandOut]:
    return get_brands(session)

@router.delete("/delete/brand")
def delete_brand_endp(
    brand_id: int,
    session: SessionDep = SessionDep
):
    return delete_brand(brand_id, session)

@router.put("/update/brand")
def update_brand_endp(
    brand_id: int,
    brand: BrandCreate,
    session: SessionDep = SessionDep
)-> BrandOut:
    return update_brand(brand_id, brand, session)

# endpoints for providers

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
    return get_providers(session)

@router.delete("/delete/provider")
def delete_provider_endp(
    provider_id: int,
    session: SessionDep = SessionDep
):
    return delete_provider(provider_id, session)

@router.put("/update/provider")
def update_provider_endp(
    provider_id: int,
    provider: ProviderUpdate,
    session: SessionDep = SessionDep
)-> ProviderOut:
    return update_provider(provider_id, provider, session)

# endpoints for category

@router.post("/create/category")
def create_categories_endp(
    category: CategoryCreate,
    session: SessionDep = SessionDep
)-> CategoryOut:
    return create_category(category, session)

@router.get("/get/category")
def get_category_endp(
    session: SessionDep = SessionDep
)-> List[CategoryOut]:
    return get_categories(session)

@router.delete("/delete/category")
def delete_category_endp(
    category_id: int,
    session: SessionDep = SessionDep
):
    return delete_category(category_id, session)

@router.put("/update/category")
def update_category_endp(
    category_id: int,
    category: CategoryUpdate,
    session: SessionDep = SessionDep
)-> CategoryOut:
    return update_category(category_id, category, session)
