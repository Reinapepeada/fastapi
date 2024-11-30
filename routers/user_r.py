from fastapi import APIRouter
from typing import List
from fastapi import Query
from database.connection.SQLConection import SessionDep, SessionDep
from database.models.SQLModels import Token, UserCreate, UserOut, UserUpdate,UserLogin
from controllers.user_c import (
    create_user,
    read_users,
    read_user,
    update_user,
    delete_user,
    login_user
)

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def get_users(session: SessionDep, offset: int = 0, limit: int = Query(100, le=100))-> List[UserOut]:
    return read_users(session=session, offset=offset, limit=limit)

@router.get("/{user_id}")
def get_user(user_id: int, session: SessionDep) -> UserOut:
    return read_user(user_id=user_id, session=session)

@router.post("/signup")
def signup(user: UserCreate, session: SessionDep) -> UserOut:
    return create_user(user_info=user, session=session)

@router.post("/login")
def login(user: UserLogin, session: SessionDep) -> Token:
    return login_user(user_info=user, session=session)

@router.put("/{user_id}", response_model=UserOut)
def modify_user(user_id: int, user: UserUpdate, session: SessionDep) -> UserOut:
    return update_user(user_id=user_id, user=user, session=session)

@router.delete("/{user_id}")
def remove_user(user_id: int, session: SessionDep) :
    return delete_user(user_id=user_id, session=session)