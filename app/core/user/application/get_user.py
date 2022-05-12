from app.core.shared.exception.base_exceptions import EntityNotFoundException
from app.core.shared.value_object.common import EntityId
from app.core.user.domain.entity.user import User
from app.core.user.domain.repository.user_repository import UserRepository


class GetUserHandler:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, user_id: EntityId) -> User:
        user = await self.user_repository.get_user(user_id)

        if not user:
            raise EntityNotFoundException(f"User id '{user_id.to_str()}' does not exist in DB")

        return user
