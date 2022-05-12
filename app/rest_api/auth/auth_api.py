from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.core.auth.auth_manager import AuthManager, TokenManager
from app.core.user.infrastructure.user_repository_postgres import UserRepositoryPostgres
from app.rest_api.auth.dto import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

auth_router = APIRouter(
    tags=["auth"],
)


@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    user = await AuthManager(UserRepositoryPostgres()).authenticate_user(email, password)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": TokenManager.create_access_token(access_token_sub=user.email),
        "token_type": "bearer",
    }
