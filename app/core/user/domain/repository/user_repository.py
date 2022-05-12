from typing import Protocol, Optional

from app.core.shared.value_object.common import EntityId
from app.core.user.domain.entity.user import User


class UserRepository(Protocol):
    async def signup_user(self, user: User):
        """Signs up User in DB"""

    async def get_user(self, user_id: EntityId) -> Optional[User]:
        """Fetches a User from DB by its Id"""

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Fetches a User from DB by its email"""

    async def delete_user(self, user_id: EntityId):
        """Deletes a User from DB by its Id"""
