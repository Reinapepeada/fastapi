from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends

# sqlite_file_name = "database.db"
postgress_railway = f"postgresql://:@fastapi.railway.internal:5432/"





# connect_args = {"check_same_thread": False}
# engine = create_engine(postgress_railway, connect_args=connect_args)
engine = create_engine(postgress_railway)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
