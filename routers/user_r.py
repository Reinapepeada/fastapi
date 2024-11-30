from fastapi import APIRouter, Header
from typing import Annotated, List
from fastapi import Query
from database.connection.SQLConection import SessionDep
from database.models.SQLModels import (
    Token,
    User,
    UserCreate,
    UserOut,
    UserUpdate,
    UserLogin,
    UserForgotPassword,
    UserResetPassword
)
from controllers.user_c import (
    create_user,
    read_users,
    read_user,
    update_user,
    delete_user,
    login_user,
    forgot_password_email,
    reset_password_email
)

router = APIRouter()


@router.get("/")
def get_users(
    session: SessionDep, offset: int = 0, limit: int = Query(100, le=100)
) -> List[User]:
    return read_users(session=session, offset=offset, limit=limit)


@router.get("/{user_id}")
def get_user(user_id: int, session: SessionDep) -> UserOut:
    return read_user(user_id=user_id, session=session)


@router.post("/signup")
def signup(user: UserCreate, session: SessionDep) -> UserOut:
    return create_user(user_info=user, session=session)


@router.post("/login")
def login(user: UserLogin, session: SessionDep) -> Token:
    return login_user(user_info=user, session=session)


@router.put("/{user_id}")
def modify_user(
    bearer_token: Annotated[str | None, Header()],
    user_id: int,
    user: UserUpdate,
    session: SessionDep,
) -> UserOut:
    return update_user(
        bearer_token=bearer_token, user_id=user_id, user=user, session=session
    )


@router.delete("/{user_id}")
def remove_user(
    bearer_token: Annotated[str | None, Header()], user_id: int, session: SessionDep
):
    return delete_user(bearer_token=bearer_token, user_id=user_id, session=session)


@router.post("/forgot-password")
def forgot_password(user: UserForgotPassword, session: SessionDep):
    return forgot_password_email(email=user.email, session=session)

@router.post("/reset-password")
def reset_password(bearer_token: Annotated[str | None, Header()], reset: UserResetPassword, session: SessionDep):
    return reset_password_email(token=bearer_token,new_password=reset.password, session=session)
