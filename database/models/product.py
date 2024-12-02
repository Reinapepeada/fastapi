from pydantic import BaseModel, EmailStr, constr
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Literal, Optional
from datetime import datetime


class Branch(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    location: str|None
    created_at: datetime = Field(default_factory=datetime.now)

    products: List["ProductVariant"] = Relationship(back_populates="branch")


class Category(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    description: str|None
    created_at: datetime = Field(default_factory=datetime.now)

    products: List["Product"] = Relationship(back_populates="category")
    discounts: List["Discount"] = Relationship(back_populates="category")


class Provider(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    contact_info: str|None
    created_at: datetime = Field(default_factory=datetime.now)

    purchases: List["Purchase"] = Relationship(back_populates="provider")
    products: List["Product"] = Relationship(back_populates="provider")

class Brand(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)

    products: List["Product"] = Relationship(back_populates="brand")


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    serial_number: str = Field(unique=True, nullable=False, index=True)
    name: str = Field(index=True, nullable=False)
    description: Optional[str] = Field(nullable=True, default=None)
    warranty_time: Optional[int]  # en días, meses o años
    cost: float = Field(nullable=False)
    wholesale_price: float = Field(nullable=False)
    retail_price: float = Field(nullable=False)
    status: str = Field(default="active")  # 'active', 'inactive', 'discontinued'
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    provider_id: Optional[int] = Field(default=None, foreign_key="provider.id")
    brand_id: Optional[int] = Field(default=None, foreign_key="brand.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    brand: Optional["Brand"] = Relationship(back_populates="products")
    category: Optional["Category"] = Relationship(back_populates="products")
    provider: Optional["Provider"] = Relationship(back_populates="products")
    images: List["ProductImage"] = Relationship(back_populates="product")
    variants: List["ProductVariant"] = Relationship(back_populates="product")
    discounts: List["Discount"] = Relationship(back_populates="product")
    purchase_items: List["PurchaseItem"] = Relationship(back_populates="product")

class ProductVariant(SQLModel, table=True):  # Variantes de productos
    id: int|None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", nullable=False)
    sku: str = Field(index=True, nullable=False)  # Código único de variante
    color: str|None =Field(nullable=True,default=None)
    size: str|None=Field(nullable=True,default=None)
    branch_id: int|None = Field(default=None, foreign_key="branch.id")
    stock: int = Field(default=0)  # Cantidad en inventario
    product: Optional["Product"] = Relationship(back_populates="variants")
    branch: Optional["Branch"] = Relationship(back_populates="products")
    order_items: List["OrderItem"] = Relationship(back_populates="products")
    product: Optional["Product"] = Relationship(back_populates="variants")
    purchase_items: List["PurchaseItem"] = Relationship(back_populates="productvariant")


class Discount(SQLModel, table=True):  # Descuentos dinámicos
    id: int|None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)  # Nombre del descuento (e.g., "Promo Navidad")
    discount_type: str = Field(nullable=False)  # 'percentage' o 'fixed'
    value: float = Field(nullable=False)  # Valor del descuento (porcentaje o fijo)
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    is_active: bool = Field(default=True)  # Estado del descuento
    product_id: int|None = Field(default=None, foreign_key="product.id")
    category_id: int|None = Field(default=None, foreign_key="category.id")
    product: Optional["Product"] = Relationship(back_populates="discounts")
    category: Optional["Category"] = Relationship(back_populates="discounts")


class ProductImage(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", nullable=False)
    image_url: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)

    product: Optional["Product"] = Relationship(back_populates="images")


# schemas de pydantic para productos
class ProductVariantCreate(BaseModel):
    product_id: int
    color: str|None
    size: str|None
    branch_id: int|None
    stock: int

    class ConfigDict:
        from_attributes = True

class ProductVariantUpdate(BaseModel):
    sku: str|None
    color: str|None
    size: str|None
    branch_id: int|None
    stock: int|None

class ProductVariantOut(BaseModel):
    product_id: int
    sku: str
    color: str|None
    size: str|None
    branch_id: int|None
    stock: int

    class ConfigDict:
        from_attributes = True

class ProductCreate(BaseModel):
    serial_number: str
    name: str
    description: str|None
    brand: int|None
    warranty_time: int|None
    cost: float
    wholesale_price: float
    retail_price: float
    status: Literal['active', 'inactive', 'discontinued']
    category_id: int|None
    provider_id: int|None
    images: Optional[List[str]]
    ProductVariant: Optional[List[ProductVariantCreate]]


class ProductUpdate(BaseModel):
    serial_number: str|None
    name: str|None
    description: str|None
    brand: int|None
    warranty_time: int|None
    cost: Optional[float]
    wholesale_price: Optional[float]
    retail_price: Optional[float]
    status: Optional[Literal['active', 'inactive', 'discontinued']]
    category_id: int|None
    provider_id: int|None
    images: Optional[List[str]]
    

class ProductOut(BaseModel):
    serial_number: str
    name: str
    description: str|None
    brand: str|None
    warranty_time: int|None
    cost: float
    wholesale_price: float
    retail_price: float
    status: Literal['active', 'inactive', 'discontinued']
    category_id: int|None
    provider_id: int|None
    images: Optional[List[str]]
    ProductVariant: Optional[List[ProductVariantCreate]]
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
    description: str|None

    class ConfigDict:
        from_attributes = True

class CategoryUpdate(BaseModel):
    name: str|None
    description: str|None

class CategoryOut(BaseModel):
    id: int
    name: str
    description: str|None
    created_at: datetime

    class ConfigDict:
        from_attributes = True


class ProviderCreate(BaseModel):
    name: str
    contact_info: str|None

    class ConfigDict:
        from_attributes = True

class ProviderUpdate(BaseModel):
    name: str|None
    contact_info: str|None

class ProviderOut(BaseModel):
    id: int
    name: str
    contact_info: str|None
    created_at: datetime

    class ConfigDict:
        from_attributes = True


class BranchCreate(BaseModel):
    name: str
    location: str|None

    class ConfigDict:
        from_attributes = True

class BranchUpdate(BaseModel):
    name: str|None
    location: str|None

class BranchOut(BaseModel):
    id: int
    name: str
    location: str|None
    created_at: datetime

    class ConfigDict:
        from_attributes = True
    
class BrandCreate(BaseModel):
    name: str

    class ConfigDict:
        from_attributes = True

class BrandOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    class ConfigDict:
        from_attributes = True