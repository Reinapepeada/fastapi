from typing import List
import uuid
from fastapi import HTTPException, status
import psycopg2
from sqlmodel import select
from database.models.product import (
    Branch,
    Category,
    Product,
    ProductImage,
    ProductOut,
    ProductUpdate,
    ProductVariant,
    ProductVariantUpdate,
    Provider,
)
from fastapi import HTTPException 
from barcode import Code128
from barcode.writer import ImageWriter
import qrcode
from services.branch_s import ensure_branch_exists
from services.brand_s import ensure_brand_exists


def ensure_category_exists(category_id: int, session):
    category = session.exec(select(Category).where(Category.id == category_id)).scalar()
    if not category:
        raise ValueError(f"Category with id {category_id} does not exist")
    return category


def ensure_provider_exists(provider_id: int, session):
    provider = session.exec(select(Provider).where(Provider.id == provider_id)).scalar()
    if not provider:
        raise ValueError(f"Provider with id {provider_id} does not exist")
    return provider


def ensure_product_exists_serial(product_serial: int, session):
    product = session.exec(
        select(Product).where(Product.serial_number == product_serial)
    ).scalar()
    if not product:
        raise ValueError(f"Product with id {product_serial} does not exist")
    return product


def ensure_product_exists_id(product_id: int, session):
    product = session.exec(select(Product).where(Product.id == product_id)).scalar()
    if not product:
        raise ValueError(f"Product with id {product_id} does not exist")
    return product


def product_exists_serial(product_serial: int, session):
    product = session.exec(
        select(Product).where(Product.serial_number == product_serial)
    ).scalar()
    if not product:
        return False
    return True


def ensure_product_variant_exists(variant_id: int, session):
    variant = session.exec(
        select(ProductVariant).where(ProductVariant.id == variant_id)
    ).scalar()
    if not variant:
        raise ValueError(f"Product variant with id {variant_id} does not exist")
    return variant


def generate_sku(product_name: str, category_id: int, provider_id: int) -> str:
    unique_id = uuid.uuid4().hex[:8].upper()
    sku = f"{product_name[:4].upper()}-{category_id:02d}-{provider_id:02d}-{unique_id}"
    return sku


def create_product_db(product, session):
    """Crea un producto o lo recupera si existe, dependiendo del flag."""
    try:
        # Validar existencia de categoría, proveedor y marca
        ensure_category_exists(product.category_id, session)
        ensure_provider_exists(product.provider_id, session)
        ensure_brand_exists(product.brand_id, session)

        db_product = product_exists_serial(product.serial_number, session)
        if not db_product:  # Crear si no existe
            db_product = Product(
                serial_number=product.serial_number,
                name=product.name,
                description=product.description,
                brand_id=product.brand_id,
                warranty_unit=product.warranty_unit,
                warranty_time=product.warranty_time,
                cost=product.cost,
                wholesale_price=product.wholesale_price,
                retail_price=product.retail_price,
                status=product.status,
                category_id=product.category_id,
                provider_id=product.provider_id,
             )
            session.add(db_product)
            session.commit()
            session.refresh(db_product)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El producto con serial {product.serial_number} ya existe.",
            )
        
        return db_product
    
    except psycopg2.IntegrityError as e:
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes crear dos productos con el mismo nombre en la misma categoría y proveedor.",
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ocurrió un error inesperado: {str(e)}"
        )


def get_products_all_db(session):
    try:
        products = session.exec(select(Product)).scalars().all()
        print(products)
        return products
    except Exception as e:
        session.rollback()
        raise e


def update_product_db(product_id: int, product: ProductUpdate, session):
    try:
        db_product = ensure_product_exists_id(product_id, session)
        # actualiza solos los campos que se le pasaron en product
        for key, value in product.model_dump(exclude_unset=True).items():
            setattr(db_product, key, value)

        session.commit()
        session.refresh(db_product)
    except Exception as e:
        session.rollback()
        raise e
    return db_product


from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func


async def fetch_products_with_filters(
    session, page: int, size: int, filters: dict
):
    """
    Fetch products with pagination and filters.
    :param session: Database session.
    :param page: Page number (1-indexed).
    :param size: Number of items per page.
    :param filters: Dictionary of filters.
    :return: Tuple of products and total count.
    """
    query = select(Product)

    # Apply filters
    if filters["categories"]:
        category_ids = [int(id_) for id_ in filters["categories"].split(",")]
        query = query.where(Product.category_id.in_(category_ids))

    if filters["brands"]:
        brand_ids = [int(id_) for id_ in filters["brands"].split(",")]
        query = query.where(Product.brand_id.in_(brand_ids))

    if filters["min_price"] is not None:
        query = query.where(Product.price >= filters["min_price"])

    if filters["max_price"] is not None:
        query = query.where(Product.price <= filters["max_price"])

    # Calculate total count
    total_query = select(func.count()).select_from(query.subquery())
    total = session.execute(total_query).scalar()

    # Fetch paginated products
    result = session.execute(
        query.offset((page - 1) * size).limit(size)
    )
    products = result.scalars().all()

    return products, total

def get_product_by_id_db(session, product_id: int):
    try:
        db_product = ensure_product_exists_id(product_id, session)
        print(db_product)
        return db_product
    except Exception as e:
        session.rollback()
        raise e

def delete_product_db(product_id: int, session):
    try:
        db_product = ensure_product_exists_id(product_id, session)
        session.delete(db_product)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    return {"msg": "Product deleted successfully"}

def ensure_unique_constraints_product_variant(product_id, color, size, size_unit, unit, session):
    variant = session.exec(
        select(ProductVariant).where(
            (ProductVariant.product_id == product_id)
            & (ProductVariant.color == color)
            & (ProductVariant.size == size)
            & (ProductVariant.size_unit == size_unit)
            & (ProductVariant.unit == unit)
        )
    ).first()
    if variant:
        raise ValueError("Ya existe una variante con las mismas de color, tamaño y unidad.")
    return variant

def create_product_variant_db(product_variants, session):
    """Crea variantes para un producto existente."""
    try:
        db_variants = []
        for variant in product_variants.variants:
            # Validar existencia de producto y sucursal
            db_product = ensure_product_exists_id(variant.product_id, session)
            ensure_branch_exists(variant.branch_id, session)
            
            # Validar unicidad de variantes
            ensure_unique_constraints_product_variant(
                variant.product_id,
                variant.color,
                variant.size,
                variant.size_unit,
                variant.unit,
                session,
            )

            # Generar SKU
            sku = generate_sku(
                product_name=db_product.name,
                category_id=db_product.category_id,
                provider_id=db_product.provider_id,
            )
            # Crear la variante
            db_variant = ProductVariant(
                product_id=variant.product_id,
                sku=sku,
                color=variant.color,
                size=variant.size,
                size_unit=variant.size_unit,
                unit=variant.unit,
                branch_id=variant.branch_id,
                stock=variant.stock,
            )
            session.add(db_variant)
            session.commit()
            session.refresh(db_variant)
            persist_product_images(variant.images, db_variant.id, session)
            db_variants.append(db_variant)
        session.commit()

        return db_variants

    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Error al crear variantes de producto: {e}")

def get_product_variants_by_product_id_db(product_id: int, session):
    try:
        db_variants = session.exec(
            select(ProductVariant).where(ProductVariant.product_id == product_id)
        ).all()
        return db_variants
    except Exception as e:
        session.rollback()
        raise e


def update_product_variant_db(variant_id: int, variant: ProductVariantUpdate, session):
    try:
        ensure_product_variant_exists(variant_id, session)
        db_variant = session.exec(
            select(ProductVariant).where(ProductVariant.id == variant_id)
        ).first()
        for key, value in variant.model_dump(exclude_unset=True).items():
            setattr(db_variant, key, value)
        session.commit()
        session.refresh(db_variant)
    except Exception as e:
        session.rollback()
        raise e
    return db_variant


def delete_product_variant_db(variant_id: int, session):
    try:
        db_variant = ensure_product_variant_exists(variant_id, session)
        session.delete(db_variant)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    return {"msg": "Variant deleted successfully"}


def persist_product_images(images, variant_id, session):
    try:
        ensure_product_variant_exists(variant_id, session)
        for url_img in images:
            session.add(ProductImage(image_url=str(url_img),variant_id=variant_id))
            session.commit()
    except Exception as e:
        session.rollback()
        raise e

def add_stock_product_variant(variant_id, quantity, session):
    try:
        db_variant = ensure_product_variant_exists(variant_id, session)
        db_variant.stock += quantity
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    return db_variant

def reduce_stock_product_variant(variant_id, quantity, session):
    try:
        db_variant = ensure_product_variant_exists(variant_id, session)
        if db_variant.stock < quantity:
            raise ValueError("No hay suficiente stock para realizar la venta")
        db_variant.stock = db_variant.stock - quantity
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    return db_variant

def generate_barcode(sku: str):
    barcode = Code128(sku, writer=ImageWriter())
    barcode.save(f"barcodes/{sku}")


def generate_qr_code(sku: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(sku)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(f"qrcodes/{sku}.png")
