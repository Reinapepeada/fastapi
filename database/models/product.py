from pydantic import BaseModel, EmailStr, constr
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Literal, Optional
from datetime import datetime


class Branch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    location: Optional[str]
    created_at: datetime = Field(default_factory=datetime.now)

    products: List["ProductVariant"] = Relationship(back_populates="branch")


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.now)

    products: List["Product"] = Relationship(back_populates="category")
    discounts: List["Discount"] = Relationship(back_populates="category")


class Provider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    contact_info: Optional[str]
    created_at: datetime = Field(default_factory=datetime.now)

    purchases: List["Purchase"] = Relationship(back_populates="provider")
    products: List["Product"] = Relationship(back_populates="provider")


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    serial_number: str = Field(unique=True, nullable=False)
    name: str = Field(index=True, nullable=False)
    description: Optional[str]
    brand: Optional[str]
    warranty_time: Optional[int]  # en días, meses o años
    cost: float = Field(nullable=False)
    wholesale_price: float = Field(nullable=False)
    retail_price: float = Field(nullable=False)
    status: str = Field(default="active")  # 'active', 'inactive', 'discontinued'
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    provider_id: Optional[int] = Field(default=None, foreign_key="provider.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    category: Optional["Category"] = Relationship(back_populates="products")
    provider: Optional["Provider"] = Relationship(back_populates="products")
    images: List["ProductImage"] = Relationship(back_populates="product")
    variants: List["ProductVariant"] = Relationship(
        back_populates="product", cascade_delete=True  )
    discounts: List["Discount"] = Relationship(back_populates="product")
    purchase_items: List["PurchaseItem"] = Relationship(back_populates="product")

class ProductVariant(SQLModel, table=True):  # Variantes de productos
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", nullable=False)
    sku: str = Field(index=True, nullable=False)  # Código único de variante
    color: Optional[str]
    size: Optional[str]
    branch_id: Optional[int] = Field(default=None, foreign_key="branch.id")
    stock: int = Field(default=0)  # Cantidad en inventario
    product: Optional["Product"] = Relationship(back_populates="variants")
    branch: Optional["Branch"] = Relationship(back_populates="products")
    order_items: List["OrderItem"] = Relationship(back_populates="products")
    product: Optional["Product"] = Relationship(back_populates="variants")
    purchase_items: List["PurchaseItem"] = Relationship(back_populates="productvariant")


class Discount(SQLModel, table=True):  # Descuentos dinámicos
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)  # Nombre del descuento (e.g., "Promo Navidad")
    discount_type: str = Field(nullable=False)  # 'percentage' o 'fixed'
    value: float = Field(nullable=False)  # Valor del descuento (porcentaje o fijo)
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    is_active: bool = Field(default=True)  # Estado del descuento
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    product: Optional["Product"] = Relationship(back_populates="discounts")
    category: Optional["Category"] = Relationship(back_populates="discounts")


class ProductImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", nullable=False)
    image_url: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)

    product: Optional["Product"] = Relationship(back_populates="images")


# schemas de pydantic para productos
class ProductVariantCreate(BaseModel):
    product_id: int
    sku: str
    color: Optional[str]
    size: Optional[str]
    branch_id: Optional[int]
    stock: int

    class Config:
        orm_mode = True

class ProductVariantUpdate(BaseModel):
    sku: Optional[str]
    color: Optional[str]
    size: Optional[str]
    branch_id: Optional[int]
    stock: Optional[int]

class ProductVariantOut(BaseModel):
    product_id: int
    sku: str
    color: Optional[str]
    size: Optional[str]
    branch_id: Optional[int]
    stock: int

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    serial_number: str
    name: str
    description: Optional[str]
    brand: Optional[str]
    warranty_time: Optional[int]
    cost: float
    wholesale_price: float
    retail_price: float
    status: Literal['active', 'inactive', 'discontinued']
    category_id: Optional[int]
    provider_id: Optional[int]
    images: Optional[List[str]]
    ProductVariant: Optional[List[ProductVariantCreate]]


class ProductUpdate(BaseModel):
    serial_number: Optional[str]
    name: Optional[str]
    description: Optional[str]
    brand: Optional[str]
    warranty_time: Optional[int]
    cost: Optional[float]
    wholesale_price: Optional[float]
    retail_price: Optional[float]
    status: Optional[Literal['active', 'inactive', 'discontinued']]
    category_id: Optional[int]
    provider_id: Optional[int]
    images: Optional[List[str]]

class ProductOut(BaseModel):
    serial_number: str
    name: str
    description: Optional[str]
    brand: Optional[str]
    warranty_time: Optional[int]
    cost: float
    wholesale_price: float
    retail_price: float
    status: Literal['active', 'inactive', 'discontinued']
    category_id: Optional[int]
    provider_id: Optional[int]
    images: Optional[List[str]]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True

class CategoryUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class ProviderCreate(BaseModel):
    name: str
    contact_info: Optional[str]

    class Config:
        orm_mode = True

class ProviderUpdate(BaseModel):
    name: Optional[str]
    contact_info: Optional[str]

class ProviderOut(BaseModel):
    id: int
    name: str
    contact_info: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class BranchCreate(BaseModel):
    name: str
    location: Optional[str]

    class Config:
        orm_mode = True

class BranchUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]

class BranchOut(BaseModel):
    id: int
    name: str
    location: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True