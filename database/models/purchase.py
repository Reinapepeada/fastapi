from pydantic import BaseModel, EmailStr, constr
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Literal, Optional
from datetime import datetime

class Purchase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    provider_id: int = Field(foreign_key="provider.id", nullable=False)
    date: datetime = Field(default_factory=datetime.now)
    total_price: float = Field(nullable=False)

    provider: Optional["Provider"] = Relationship(back_populates="purchases")
    items: List["PurchaseItem"] = Relationship(back_populates="purchase")

class PurchaseItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", nullable=False)
    purchase_id: int = Field(foreign_key="purchase.id", nullable=False)
    productvariant_id: int = Field(foreign_key="productvariant.id", nullable=False)
    quantity: int = Field(nullable=False)
    cost: float = Field(nullable=False)
    total_cost: float = Field(nullable=False)

    product: Optional["Product"] = Relationship(back_populates="purchase_items")
    productvariant: Optional["ProductVariant"] = Relationship(back_populates="purchase_items")
    purchase: Optional["Purchase"] = Relationship(back_populates="items")
