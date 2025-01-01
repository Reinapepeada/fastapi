from fastapi import APIRouter
from typing import List
from controllers.product_c import create_provider, delete_provider, get_providers, update_provider
from database.connection.SQLConection import SessionDep

from database.models.product import (
    ProviderCreate,
    ProviderOut)
# enpoints for provideres
router = APIRouter()

@router.post("/create")
def create_provider_endp(
    provider: ProviderCreate,
    session: SessionDep = SessionDep
):
    return create_provider(provider, session)

@router.get("/get/all")
def get_provider_endp(
    session: SessionDep = SessionDep
)-> List[ProviderOut]:
    return get_providers(session)

@router.delete("/delete")
def delete_provider_endp(
    provider_id: int,
    session: SessionDep = SessionDep
):
    return delete_provider(provider_id, session)

@router.put("/update")
def update_provider_endp(
    provider_id: int,
    provider: ProviderCreate,
    session: SessionDep = SessionDep
)-> ProviderOut:
    return update_provider(provider_id, provider, session)