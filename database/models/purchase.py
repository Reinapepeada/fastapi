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



class CreatePurchaseItem(BaseModel):
    product_id: int
    productvariant_id: int
    purchase_id: int
    quantity: int
    cost: float
    # total_cost: float hacer calculo en backend

class CreatePurchase(BaseModel):
    provider_id: int
    # total_price: float hacer calculo en backend
    items: List[CreatePurchaseItem]

class UpdatePurchaseItem(BaseModel):
    quantity: Optional[int]
    cost: Optional[float]
    # total_cost: Optional[float] hacer calculo en backend

class UpdatePurchase(BaseModel):
    provider_id: Optional[int] = None
    total_price: Optional[float] = None 
    items: Optional[List[UpdatePurchaseItem]] = None

class PurchaseItemResponse(BaseModel):
    id: int
    product_id: int
    productvariant_id: int
    quantity: int
    cost: float
    total_cost: float


class PurchaseResponse(BaseModel):
    id: int
    provider_id: int
    date: datetime
    total_price: float
    items: List[PurchaseItemResponse]