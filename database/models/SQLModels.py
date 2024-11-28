from pydantic import BaseModel,EmailStr,constr
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Literal, Optional
from datetime import datetime

# crear clase de sqlmodel para usuarios
class User(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    dni: str = Field( index=True, nullable=False , unique=True)
    first_name: str = Field(index=True, nullable=False)
    last_name: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)
    password_hash: str = Field(nullable=False)
    phone: str = Field(nullable=True)
    role: str = Field(default="user", nullable=False)  # 'admin' o 'user'
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_adress: str = Field(nullable=True)
    orders: List["Order"] = Relationship(back_populates="user")
    audits: List["Audit"] = Relationship(back_populates="admin")

# crear clase de pydantic para registro de usuarios
class UserCreate(BaseModel):
    first_name: str = constr(min_length=3, max_length=50)
    last_name: str = constr(min_length=3, max_length=50)
    dni: str 
    email: EmailStr
    role : Literal['admin','user']
    phone: str 
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
    first_name: Optional[str] = None | constr(min_length=3, max_length=50)
    last_name: Optional[str] = None| constr(min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

# crear clase de pydantic para devolver informacion de usuarios
class UserOut(BaseModel):
    first_name: str
    last_name: str
    dni: str
    email: EmailStr
    role: Literal['user','admin']
    phone: str
    created_at: datetime
    updated_at: datetime

# crear clase de pydantic para  eliminacion de usuarios
class UserDelete(BaseModel):
    dni: str

class Branch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    location: str
    created_at: datetime = Field(default_factory=datetime.now)

    products: List["Product"] = Relationship(back_populates="branch")


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    products: List["Product"] = Relationship(back_populates="category")


class Provider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    contact_info: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    products: List["Product"] = Relationship(back_populates="provider")


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    serial_number: str = Field(unique=True, nullable=False)
    name: str = Field(index=True, nullable=False)
    description: Optional[str] = None
    color: Optional[str] = None
    brand: Optional[str] = None
    warranty_time: Optional[int] = None  # en días, meses o años
    cost: float = Field(nullable=False)
    wholesale_price: float = Field(nullable=False)
    retail_price: float = Field(nullable=False)
    stock: int = Field(default=0)
    status: str = Field(default="active")  # 'active', 'inactive', 'discontinued'
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    provider_id: Optional[int] = Field(default=None, foreign_key="provider.id")
    branch_id: Optional[int] = Field(default=None, foreign_key="branch.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    category: Optional["Category"] = Relationship(back_populates="products")
    provider: Optional["Provider"] = Relationship(back_populates="products")
    branch: Optional["Branch"] = Relationship(back_populates="products")
    images: List["ProductImage"] = Relationship(back_populates="product")
    order_items: List["OrderItem"] = Relationship(back_populates="product")


class ProductImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", nullable=False)
    image_url: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)

    product: Optional["Product"] = Relationship(back_populates="images")


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    status: str = Field(default="pending")  # 'pending', 'processing', 'completed', 'cancelled'
    total_price: float = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id", nullable=False)
    product_id: int = Field(foreign_key="product.id", nullable=False)
    quantity: int = Field(nullable=False)
    price: float = Field(nullable=False)

    order: Optional["Order"] = Relationship(back_populates="items")
    product: Optional["Product"] = Relationship(back_populates="order_items")


class Audit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    admin_id: int = Field(foreign_key="user.id", nullable=False)
    action: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)

    admin: Optional["User"] = Relationship(back_populates="audits")