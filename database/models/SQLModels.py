from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)
    password_hash: str = Field(nullable=False)
    role: str = Field(default="user", nullable=False)  # 'admin' o 'user'
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    orders: List["Order"] = Relationship(back_populates="user")
    audits: List["Audit"] = Relationship(back_populates="admin")


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