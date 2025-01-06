
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends
import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
postgress_railway = os.getenv("DATABASE_URL")


# connect_args = {"check_same_thread": False}
# engine = create_engine(postgress_railway, connect_args=connect_args)
# async_engine = create_async_engine(postgress_railway, echo=True)
engine = create_engine(postgress_railway)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



# async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# async def get_async_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session


def get_session():
    with Session(engine) as session:
        yield session



SessionDep = Annotated[Session, Depends(get_session)]
# AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]