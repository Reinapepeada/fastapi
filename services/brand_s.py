
from sqlmodel import select
from database.models.product import Brand, BrandCreate

def ensure_brand_exists(brand_id: int, session):
    brand = session.exec(select(Brand).where(Brand.id == brand_id)).first()
    if not brand:
        raise ValueError(f"brand with id {brand_id} does not exist")
    return brand

def create_brand_db(brand: BrandCreate, session):
    try:
        db_brand = Brand(
            name=brand.name,
        )
        session.add(db_brand)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

    return db_brand

def delete_brand_db(brand_id: int, session):
    try:
        db_brand = ensure_brand_exists(brand_id, session)
        session.delete(db_brand)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def update_brand_db(brand_id: int, brand: BrandCreate, session):
    try:
        ensure_brand_exists(brand_id, session)
        db_brand = session.exec(select(Brand).where(Brand.id == brand_id)).first()
        for key, value in brand.model_dump(exclude_unset=True).items():
            setattr(db_brand, key, value)
        session.commit()
        session.refresh(db_brand)
    except Exception as e:
        session.rollback()
        raise e
    return db_brand

def get_brands_all(session):
    try:
        brands = session.exec(select(Brand)).all()
        return brands
    except Exception as e:
        session.rollback()
        raise e