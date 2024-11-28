from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from sqlmodel import SQLModel, select
from database.connection.SQLConection import SessionDep, create_db_and_tables, SessionDep, drop_db_and_tables
from sqlalchemy.exc import SQLAlchemyError
from database.models.SQLModels import User, UserCreate, UserOut, UserUpdate
import os
import uvicorn

load_dotenv()

app = FastAPI()


# borrar la base de datos y volverla a crear
# @app.on_event("startup")
# def on_startup():
#     drop_db_and_tables()
#     create_db_and_tables()

@app.get("/")
def read_root():
    create_db_and_tables()
    return {"msg": "Welcome to team celular's API!"}


@app.post("/signup/")
def create_user(user: UserCreate, session: SessionDep) -> UserOut:
    try:
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            dni=user.dni,
            email=user.email,
            role=user.role,
            phone=user.phone,
            password_hash=user.password
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users/")
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, session: SessionDep) -> UserOut:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/user_id")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, session: SessionDep) -> UserOut:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    data = user.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_user, key, value)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

