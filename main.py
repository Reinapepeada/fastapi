from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from sqlmodel import SQLModel, select
from database.connection.SQLConection import SessionDep, create_db_and_tables, SessionDep, drop_db_and_tables
from sqlalchemy.exc import SQLAlchemyError
from database.models.SQLModels import User, UserCreate, UserOut, UserUpdate
from routers import user_r

load_dotenv()

app = FastAPI()

app.include_router(user_r.router, tags=["Users"], prefix="/users")
# borrar la base de datos y volverla a crear
@app.on_event("startup")
def on_startup():
    print("Starting up")
    print(SQLModel.metadata)
    drop_db_and_tables()
    # create_db_and_tables()



@app.get("/")
def read_root():
    create_db_and_tables()
    return {"msg": "Welcome to team celular's API!"}




