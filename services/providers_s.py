
from sqlmodel import select
from database.models.product import Provider, ProviderCreate

def ensure_provider_exists(provider_id: int, session):
    provider = session.exec(select(Provider).where(Provider.id == provider_id)).first()
    if not provider:
        raise ValueError(f"provider with id {provider_id} does not exist")
    return provider

def create_provider_db(provider: ProviderCreate, session):
    try:
        db_provider = Provider(
            name= provider.name,
            contact_info= provider.contact_info,
        )
        session.add(db_provider)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

    return db_provider

def delete_provider_db(provider_id: int, session):
    try:
        db_provider = ensure_provider_exists(provider_id, session)
        session.delete(db_provider)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def update_provider_db(provider_id: int, provider: ProviderCreate, session):
    try:
        ensure_provider_exists(provider_id, session)
        db_provider = session.exec(select(Provider).where(Provider.id == provider_id)).first()
        for key, value in provider.model_dump(exclude_unset=True).items():
            setattr(db_provider, key, value)
        session.commit()
        session.refresh(db_provider)
    except Exception as e:
        session.rollback()
        raise e
    return db_provider

def get_providers_all(session):
    try:
        providers = session.exec(select(Provider)).all()
        return providers
    except Exception as e:
        session.rollback()
        raise e