from fastapi import APIRouter
from typing import List
from controllers.product_c import create_branch, delete_branch, get_branches, update_branch
from database.connection.SQLConection import SessionDep

from database.models.product import (
    BranchCreate,
    BranchOut)
# enpoints for branches
router = APIRouter()

@router.post("/create")
def create_branch_endp(
    branch: BranchCreate,
    session: SessionDep = SessionDep
):
    return create_branch(branch, session)

@router.get("/get/all")
def get_branch_endp(
    session: SessionDep = SessionDep
)-> List[BranchOut]:
    return get_branches(session)

@router.delete("/delete")
def delete_branch_endp(
    branch_id: int,
    session: SessionDep = SessionDep
):
    return delete_branch(branch_id, session)

@router.put("/update")
def update_branch_endp(
    branch_id: int,
    branch: BranchCreate,
    session: SessionDep = SessionDep
):
    return update_branch(branch_id, branch, session)