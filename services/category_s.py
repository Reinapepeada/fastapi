
from sqlmodel import select
from database.models.product import Category, CategoryCreate

def ensure_category_exists(category_id: int, session):
    category = session.exec(select(Category).where(Category.id == category_id)).first()
    if not category:
        raise ValueError(f"category with id {category_id} does not exist")
    return category

def create_category_db(category: CategoryCreate, session):
    try:
        db_category = Category(
            name=category.name,
            description=category.description      
        )
        session.add(db_category)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

    return db_category

def delete_category_db(category_id: int, session):
    try:
        db_category = ensure_category_exists(category_id, session)
        session.delete(db_category)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def update_category_db(category_id: int, category: CategoryCreate, session):
    try:
        ensure_category_exists(category_id, session)
        db_category = session.exec(select(Category).where(Category.id == category_id)).first()
        for key, value in category.model_dump(exclude_unset=True).items():
            setattr(db_category, key, value)
        session.commit()
        session.refresh(db_category)
    except Exception as e:
        session.rollback()
        raise e
    return db_category

def get_categories_all_db(session):
    try:
        categorys = session.exec(select(Category)).all()
        return categorys
    except Exception as e:
        session.rollback()
        raise e