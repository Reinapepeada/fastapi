from pydantic import BaseModel, EmailStr, constr
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Literal, Optional
from datetime import datetime


# crear clase de sqlmodel para usuarios
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dni: str = Field(index=True, nullable=False, unique=True)
    first_name: str = Field(index=True, nullable=False)
    last_name: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)
    password_hash: str = Field(nullable=False)
    phone: Optional[str] = Field(nullable=True)
    role: str = Field(default="user", nullable=False)  # 'admin' o 'user'
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_adress: Optional[str] = Field(nullable=True)
    orders: List["Order"] = Relationship(back_populates="user")
    audits: List["Audit"] = Relationship(back_populates="admin")

class Audit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    admin_id: int = Field(foreign_key="user.id", nullable=False)
    action: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)

    admin: Optional["User"] = Relationship(back_populates="audits")
# crear clase de pydantic para registro de usuarios
class UserCreate(BaseModel):
    first_name: str = constr(min_length=3, max_length=50)
    last_name: str = constr(min_length=3, max_length=50)
    dni: str
    email: EmailStr
    role: Literal['admin', 'user']
    phone: Optional[str]
    password: str = constr(min_length=8)

# crear clase de pydantic para login de usuarios
class UserLogin(BaseModel):
    email: EmailStr
    password: str = constr(min_length=8)

# crear clase de pydantic para devolver token de autenticacion
class Token(BaseModel):
    access_token: str
    token_type: str

# crear clase de pydantic para actualizar usuarios
class UserUpdate(BaseModel):
    first_name: Optional[str] = constr(min_length=3, max_length=50)
    last_name: Optional[str] = constr(min_length=3, max_length=50)
    email: Optional[EmailStr]
    phone: Optional[str]

# crear clase de pydantic para devolver informacion de usuarios
class UserOut(BaseModel):
    first_name: str
    last_name: str
    dni: str
    email: EmailStr
    role: Literal['user', 'admin']
    phone: Optional[str]
    created_at: datetime
    updated_at: datetime

# crear clase de pydantic para eliminacion de usuarios
class UserDelete(BaseModel):
    dni: str

class UserForgotPassword(BaseModel):
    email: EmailStr

class UserResetPassword(BaseModel):
    password: str = constr(min_length=8)
