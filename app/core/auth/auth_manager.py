from datetime import timedelta, datetime
from http import HTTPStatus

import jwt
from fastapi import HTTPException

from app.core.auth.password_manager import PasswordManager
from app.core.user.domain.entity.user import User
from app.core.user.domain.repository.user_repository import UserRepository
from config.settings import get_settings

ALGORITHM = "HS256"
TOKEN_TYPE = "access_token"
settings = get_settings()


class AuthManager:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_repository.get_user_by_email(email)

        # throw exceptions
        if not user:
            return False

        if not PasswordManager.verify_password(password, user.hashed_password):
            return False

        return user

    async def get_current_user(self, token: str) -> User:
        credentials_error = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if email is None:
                raise credentials_error

            user = await self.user_repository.get_user_by_email(email)
            if user is None:
                raise credentials_error
        except Exception:
            raise credentials_error

        return user


class TokenManager:
    @staticmethod
    def create_access_token(access_token_sub: str) -> str:
        access_token_expiration = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        payload = {
            "type": TOKEN_TYPE,
            "exp": access_token_expiration,
            "iat": datetime.utcnow(),
            "sub": access_token_sub,
        }

        return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)
