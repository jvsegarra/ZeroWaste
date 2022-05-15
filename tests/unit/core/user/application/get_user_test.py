from unittest import mock

import pytest

from app.core.shared.exception.base_exceptions import EntityNotFoundException
from app.core.shared.value_object.common import EntityId
from app.core.user.application.get_user import GetUserHandler
from app.core.user.domain.entity.user import User
from app.core.user.domain.repository.user_repository import UserRepository
from app.core.user.domain.value_object.user_value_object import PersonalInfo, UserType


@pytest.mark.asyncio
class TestGetuser:
    def setup(self) -> None:
        self.user_repository = mock.create_autospec(UserRepository)
        self.get_user_handler = GetUserHandler(self.user_repository)

    async def test_get_user_returns_user_successfully(self) -> None:
        # Given
        requested_user_id = EntityId(EntityId.new())
        requested_user = User(
            entity_id=requested_user_id,
            email="test@zw.com",
            hashed_password="hashed password",
            personal_info=PersonalInfo("first_name", "last name"),
            user_type=UserType.RIDER,
        )
        self.user_repository.get_user.return_value = requested_user

        # When
        response = await self.get_user_handler.handle(requested_user_id)

        # Then
        assert response == requested_user

    async def test_get_user_throws_exception_when_user_does_not_exist(self) -> None:
        # Given
        requested_user_id = EntityId(EntityId.new())
        self.user_repository.get_user.return_value = None

        # When - Then
        with pytest.raises(
            EntityNotFoundException, match=f"User id '{requested_user_id.to_str()}' does not exist in DB"
        ):
            await self.get_user_handler.handle(requested_user_id)
