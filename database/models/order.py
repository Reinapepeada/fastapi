from pydantic import BaseModel, EmailStr, constr
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Literal, Optional
from datetime import datetime



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
    productvariant_id: int = Field(foreign_key="productvariant.id", nullable=False)
    quantity: int = Field(nullable=False)
    price: float = Field(nullable=False)

    order: Optional["Order"] = Relationship(back_populates="items")
    products: Optional["ProductVariant"] = Relationship(back_populates="order_items")