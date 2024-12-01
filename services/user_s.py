from sqlalchemy.orm import Session
from database.models.user import UserCreate, UserUpdate, User
from services import auth_s
from fastapi import HTTPException

def get_all_users(session: Session, email: str = None, offset: int = 0, limit: int = 100):
    query = session.query(User)
    if email:
        query = query.filter(User.email == email)
    return query.offset(offset).limit(limit).all()

def get_user_by_email(email: str, session: Session):
    return session.query(User).filter(User.email == email).first()

def authenticate_user(email: str, password: str, session: Session):
    user = get_user_by_email(email=email, session=session)
    if not user:
        return False
    if not auth_s.verify_password(password, user.password_hash):
        return False
    return user

def get_user_by_id(user_id: int, session: Session):
    return session.query(User).filter(User.id == user_id).first()

def create_new_user(user: UserCreate, session: Session):
    db_user = User(
        email=user.email,
        password_hash=auth_s.get_password_hash(user.password),
        role=user.role,
        dni=user.dni,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def update_existing_user(user_id: int, user: UserUpdate, session: Session):
    db_user = session.query(User).filter(User.id == user_id).first()
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    session.commit()
    session.refresh(db_user)
    return db_user

# verificar que al actualizar o eliminar un usuario, el usuario que hace la petición sea un administrador o el mismo usuario
def verify_user_permissions(token: str, user_id: int, session: Session):
    user_email, user_role = auth_s.get_current_user(token)
    if not user_email:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    
    if user_role == "admin":
        return True
    
    user = get_user_by_id(user_id=user_id, session=session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.email == user_email:
        return True
    
    return False


def remove_user_by_id(user_id: int, session: Session):
    user = session.query(User).filter(User.id == user_id).first()
    session.delete(user)
    session.commit()
    return {"ok": True}

def change_password(user_id: int, new_password: str, session: Session):
    user = session.query(User).filter(User.id == user_id).first()
    # print(user)
    new_hashed_password = auth_s.get_password_hash(new_password)
    # print(new_hashed_password)
    user.password_hash = new_hashed_password
    session.commit()
    return {"ok": True}