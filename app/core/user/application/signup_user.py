from pydantic import EmailStr
from pydantic.dataclasses import dataclass

from app.core.shared.value_object.common import EntityId
from app.core.user.domain.entity.user import User
from app.core.user.domain.repository.user_repository import UserRepository
from app.core.user.domain.value_object.user_value_object import UserType, PersonalInfo
from app.core.auth.password_manager import PasswordManager


@dataclass
class PersonalInfoCommand:
    first_name: str
    last_name: str


@dataclass
class SignupUserCommand:
    email: EmailStr
    password: str
    personal_info: PersonalInfoCommand
    user_type: UserType


class SignupUserHandler:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, command: SignupUserCommand) -> EntityId:
        hashed_password = PasswordManager.hash_password(command.password)

        user = User(
            entity_id=EntityId(EntityId.new()),
            email=command.email,
            hashed_password=hashed_password,
            personal_info=PersonalInfo(
                first_name=command.personal_info.first_name, last_name=command.personal_info.last_name
            ),
            user_type=command.user_type,
        )

        await self.user_repository.signup_user(user)

        return user.id
