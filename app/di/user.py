from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.auth.auth_manager import AuthManager
from app.core.user.application.delete_user import DeleteUserHandler
from app.core.user.application.get_user import GetUserHandler
from app.core.user.application.signup_user import SignupUserHandler
from app.core.user.domain.entity.user import User
from app.core.user.infrastructure.user_repository_postgres import UserRepositoryPostgres

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return await AuthManager(UserRepositoryPostgres()).get_current_user(token=token)


async def get_signup_user_handler():
    handler = SignupUserHandler(UserRepositoryPostgres())
    yield handler


async def get_get_user_handler():
    handler = GetUserHandler(UserRepositoryPostgres())
    yield handler


async def get_delete_user_handler():
    handler = DeleteUserHandler(UserRepositoryPostgres())
    yield handler
