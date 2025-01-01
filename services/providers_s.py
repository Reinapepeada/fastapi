
from sqlmodel import select
from database.models.product import Provider, ProviderCreate

def ensure_provider_exists(provider_id: int, session):
    provider = session.exec(select(Provider).where(Provider.id == provider_id)).first()
    if not provider:
        raise ValueError(f"provider with id {provider_id} does not exist")
    return provider

def unique_constraint_provider(provider: ProviderCreate, session):
    provider = session.exec(select(Provider).where(Provider.name == provider.name)).first()
    if provider:
        raise ValueError(f"Proveedor con name '{provider.name}' ya existe")
    provider = session.exec(select(Provider).where(Provider.email == provider.email)).first()
    if provider:
        raise ValueError(f"Proveedor con email '{provider.email}' ya existe")
    provider = session.exec(select(Provider).where(Provider.phone == provider.phone)).first()
    if provider:
        raise ValueError(f"Proveedor con phone '{provider.phone}' ya existe")

    return True

def create_provider_db(provider: ProviderCreate, session):
    try:
        unique_constraint_provider(provider, session)
        db_provider = Provider(
            name= provider.name,
            email= provider.email,
            phone= provider.phone,
            address= provider.address,
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
        unique_constraint_provider(provider, session)
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