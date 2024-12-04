from pydantic import BaseModel, EmailStr, constr
from sqlmodel import Field, SQLModel, Relationship,Enum as Eenum ,UniqueConstraint
from typing import List, Literal, Optional
from datetime import datetime
from enum import Enum



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


class ProductStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"


class SizeUnit(str, Enum):
    CLOTHING = "clothing"  # Tallas de ropa (e.g., S, M, L)
    DIMENSIONS = "dimensions"  # Dimensiones (e.g., cm, m)
    WEIGHT = "weight"  # Peso (e.g., kg, g)
    OTHER = "other"  # Otros

class Unit (str, Enum):
    
    # Medidas de peso
    KG = "kg"
    G = "g"
    LB = "lb"
    
    # Medidas de longitud
    cm = "cm"
    m = "m"
    inch= "inch"
    
    # Tallas de ropa
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    serial_number: str = Field(unique=True, nullable=False, index=True)
    name: str = Field(index=True, nullable=False)
    description: Optional[str] = Field(nullable=True, default=None)
    warranty_time: Optional[int] = Field(nullable=True)  # Valor del tiempo de garantía
    warranty_unit: Optional[str] = Field(default="days")  # 'days', 'months', 'years'
    cost: float = Field(nullable=False)
    wholesale_price: float = Field(nullable=False)
    retail_price: float = Field(nullable=False)
    status: ProductStatus = Eenum(ProductStatus, nullable=False)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    provider_id: Optional[int] = Field(default=None, foreign_key="provider.id")
    brand_id: Optional[int] = Field(default=None, foreign_key="brand.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relaciones
    brand: Optional["Brand"] = Relationship(back_populates="products")
    category: Optional["Category"] = Relationship(back_populates="products")
    provider: Optional["Provider"] = Relationship(back_populates="products")
    variants: List["ProductVariant"] = Relationship(back_populates="product", cascade_delete=True)
    discounts: List["Discount"] = Relationship(back_populates="product")
    purchase_items: List["PurchaseItem"] = Relationship(back_populates="product")


class ProductVariant(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("product_id", "color", "size", "size_unit", name="unique_variant_constraint"),
    )
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", nullable=False)
    sku: str = Field(index=True, nullable=False, unique=True)
    color: str | None = Field(nullable=True, default=None, index=True)
    size: str | None = Field(nullable=True, default=None, index=True)
    size_unit: SizeUnit = Eenum(SizeUnit, nullable=True, default=None)
    unit: Unit = Eenum(Unit, nullable=False)
    branch_id: int | None = Field(default=None, foreign_key="branch.id")
    stock: int = Field(default=0, index=True)
    min_stock: int = Field(default=5, index=True)  # Para alertar stock bajo
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relaciones
    product: Optional["Product"] = Relationship(back_populates="variants")
    images: List["ProductImage"] = Relationship(back_populates="variant", cascade_delete=True)
    branch: Optional["Branch"] = Relationship(back_populates="products")
    order_items: List["OrderItem"] = Relationship(back_populates="products")
    purchase_items: List["PurchaseItem"] = Relationship(back_populates="productvariant")


class ProductImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    variant_id: int = Field(foreign_key="productvariant.id", nullable=False)
    image_url: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relaciones
    variant: Optional["ProductVariant"] = Relationship(back_populates="images")


class Discount(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    discount_type: str = Field(nullable=False)  # 'percentage' o 'fixed'
    value: float = Field(nullable=False)  # Valor del descuento
    start_date: Optional[datetime] = Field(nullable=True)
    end_date: Optional[datetime] = Field(nullable=True)
    is_active: bool = Field(default=True)
    product_id: int | None = Field(default=None, foreign_key="product.id")
    category_id: int | None = Field(default=None, foreign_key="category.id")

    # Relaciones
    product: Optional["Product"] = Relationship(back_populates="discounts")
    category: Optional["Category"] = Relationship(back_populates="discounts")




# schemas de pydantic para productos
class ProductVariantCreate(BaseModel):
    product_id: int
    color: str|None
    size: str|None
    size_unit: SizeUnit|None
    unit: Unit
    branch_id: int|None
    stock: int
    min_stock: int
    images: Optional[List[str]] = None

    class ConfigDict:
        from_attributes = True

class ProductVariantCreateList(BaseModel):
    variants: List[ProductVariantCreate]
    
    class ConfigDict:
        from_attributes = True


class ProductVariantUpdate(BaseModel):
    color: str|None= None
    size: str|None= None
    size: str|None= None
    size_unit: SizeUnit|None= None
    unit: Unit = None
    branch_id: int|None= None
    stock: int|None= None
    images: Optional[List[str]] = None

class ProductVariantOut(BaseModel):
    id: int
    product_id: int
    sku: str
    color: str|None
    size: str|None
    size_unit: SizeUnit|None
    unit: Unit
    branch_id: int|None
    stock: int
    created_at: datetime
    updated_at: datetime
    images: Optional[List[str]] = None

    class ConfigDict:
        from_attributes = True

class ProductCreate(BaseModel):
    serial_number: str 
    name: str
    description: str|None
    brand_id: int|None = None
    warranty_time: int|None = None
    cost: float
    wholesale_price: float
    retail_price: float
    status: ProductStatus |None = None
    category_id: int|None = None
    provider_id: int|None = None
    


class ProductUpdate(BaseModel):
    serial_number: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    brand_id: Optional[int] = None
    warranty_time: Optional[int] = None
    cost: Optional[float] = None
    wholesale_price: Optional[float] = None
    retail_price: Optional[float] = None
    status: Optional[ProductStatus] = None
    category_id: Optional[int] = None
    provider_id: Optional[int] = None

    class ConfigDict:
        from_attributes = True
    

class ProductOut(BaseModel):
    id: int
    serial_number: str
    name: str
    description: str|None
    brand_id: int|None
    warranty_time: int|None
    cost: float
    wholesale_price: float
    retail_price: float
    status: ProductStatus 
    category_id: int|None
    provider_id: int|None
    variants: Optional[List[ProductVariantCreate]]

    class ConfigDict:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
    description: str|None

    class ConfigDict:
        from_attributes = True

class CategoryUpdate(BaseModel):
    name: str|None=None
    description: str|None=None

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
    name: str|None=None
    contact_info: str|None=None

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
    name: str|None=None
    location: str|None=None

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