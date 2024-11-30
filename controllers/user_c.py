from fastapi import HTTPException
from sqlalchemy.orm import Session
from services.user_s import (
    get_all_users,
    get_user_by_id,
    create_new_user,
    update_existing_user,
    remove_user_by_id,
    authenticate_user,
)

from services.auth_s import create_access_token
from database.models.SQLModels import UserCreate, UserLogin, UserUpdate,Token

def create_user(user_info: UserCreate, session: Session):
    existing_user = get_all_users(session=session, email=user_info.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return create_new_user(user=user_info, session=session)

def login_user(user_info: UserLogin, session: Session):
    
    user = authenticate_user(session=session, email=user_info.email, password=user_info.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Crear el token y establecerlo en una cookie
    token = create_access_token(data={"sub": user.email, "role": user.role, "id": user.id})
    
    return Token(access_token=token, token_type="bearer")
        
def read_users(session: Session, offset: int, limit: int):
    return get_all_users(session=session, offset=offset, limit=limit)

def read_user(user_id: int, session: Session):
    user = get_user_by_id(user_id=user_id, session=session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
def update_user(user_id: int, user: UserUpdate, session: Session):
    existing_user = get_user_by_id(user_id=user_id, session=session)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    return update_existing_user(user_id=user_id, user=user, session=session)

def delete_user(user_id: int, session: Session):
    user = get_user_by_id(user_id=user_id, session=session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return remove_user_by_id(user_id=user_id, session=session)