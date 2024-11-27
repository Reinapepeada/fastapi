
from sqlmodel import Field, SQLModel
import datetime


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    full_name: constr(min_length=1, max_length=100)
    email: EmailStr = Field(index=True, unique=True)
    password_hash: str
    phone_number: Optional[constr(max_length=20)] = None
    address: Optional[str] = None
    creation_date: datetime = Field(default_factory=datetime.timezone.utc)
    status: str = Field(default="active")  # 'active' or 'inactive' 
