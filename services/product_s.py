
import uuid

from sqlmodel import select
from database.models.product import Branch, Category, Product, ProductVariant, Provider
from barcode import Code128
from barcode.writer import ImageWriter
import qrcode


def ensure_category_exists(category_id: int, session):
    category = session.exec(select(Category).where(Category.id == category_id)).first()
    if not category:
        raise ValueError(f"Category with id {category_id} does not exist")
    return category

def ensure_provider_exists(provider_id: int, session):
    provider = session.exec(select(Provider).where(Provider.id == provider_id)).first()
    if not provider:
        raise ValueError(f"Provider with id {provider_id} does not exist")
    return provider
def ensure_branch_exists(branch_id: int, session):
    branch = session.exec(select(Branch).where(Branch.id == branch_id)).first()
    if not branch:
        raise ValueError(f"Branch with id {branch_id} does not exist")
    return branch

def ensure_product_exists(product_id: int, session):
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    if not product:
        raise ValueError(f"Product with id {product_id} does not exist")
    return product

def generate_sku(product_name: str, category_id: int, provider_id: int) -> str:
    unique_id = uuid.uuid4().hex[:8].upper()
    sku = f"{product_name[:4].upper()}-{category_id:02d}-{provider_id:02d}-{unique_id}"
    return sku

def create_product_and_variants(product, session, create_product_if_not_exists=True):
    """Crea un producto y sus variantes, o solo agrega variantes si el producto ya existe."""
    try:
        # Validar categoría y proveedor
        category = ensure_category_exists(product.category_id, session)
        provider = ensure_provider_exists(product.provider_id, session)

        # Intentar recuperar o crear el producto
        db_product = None
        if create_product_if_not_exists:
            db_product = ensure_product_exists(product.id, session)
            if not db_product:
                db_product = Product(
                    name=product.name,
                    description=product.description,
                    category_id=product.category_id,
                    provider_id=product.provider_id,
                    serial_number=product.serial_number,
                    brand=product.brand,
                    warranty_time=product.warranty_time,
                    cost=product.cost,
                    wholesale_price=product.wholesale_price,
                    retail_price=product.retail_price,
                    status=product.status,
                )
                session.add(db_product)
                session.commit()
                session.refresh(db_product)
        else:
            db_product = ensure_product_exists(product.id, session)
            if not db_product:
                raise ValueError("Product does not exist, and `create_product_if_not_exists` is False.")

        # Crear variantes
        for variant in product.ProductVariant:
            sku = generate_sku(
                product_name=product.name,
                category_id=product.category_id,
                provider_id=product.provider_id,
            )
            db_variant = ProductVariant(
                product_id=db_product.id,
                sku=sku,
                color=variant.color,
                size=variant.size,
                branch_id=variant.branch_id,
                stock=variant.stock,
            )
            session.add(db_variant)
        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    return db_product

    
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
    img = qr.make_image(fill='black', back_color='white')
    img.save(f"qrcodes/{sku}.png")

def create_category_db(category, session):
    try:
        db_category = Category(
            name=category.name,
            description=category.description
        )
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
    except Exception as e:
        session.rollback()
        raise e
    
def get_category_all(session):
    categories = session.exec(select(Category)).all()
    print(categories)
    return categories

def create_provider_db(provider, session):
    try:
        db_provider = Provider(
            name=provider.name,
            contact_info=provider.contact_info,
        )
        session.add(db_provider)
        session.commit()
        session.refresh(db_provider)
    except Exception as e:
        session.rollback()
        raise e

def get_provider_all(session):
    providers = session.exec(select(Provider)).all()
    return providers