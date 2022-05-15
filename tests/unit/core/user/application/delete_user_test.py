from unittest import mock

import pytest

from app.core.shared.exception.base_exceptions import EntityNotFoundException, InvalidStatusException
from app.core.shared.value_object.common import EntityId, EntityStatus
from app.core.user.application.delete_user import DeleteUserHandler
from app.core.user.domain.entity.user import User
from app.core.user.domain.repository.user_repository import UserRepository
from app.core.user.domain.value_object.user_value_object import PersonalInfo, UserType


@pytest.mark.asyncio
class TestDeleteuser:
    def setup(self) -> None:
        self.user_repository = mock.create_autospec(UserRepository)
        self.delete_user_handler = DeleteUserHandler(self.user_repository)

    async def test_delete_user_successfully(self) -> None:
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
        await self.delete_user_handler.handle(requested_user_id)

        # Then
        self.user_repository.delete_user.assert_called_once_with(requested_user_id)

    async def test_get_user_throws_exception_when_user_does_not_exist(self) -> None:
        # Given
        requested_user_id = EntityId(EntityId.new())
        self.user_repository.get_user.return_value = None

        # When - Then
        with pytest.raises(
            EntityNotFoundException, match=f"User id '{requested_user_id.to_str()}' does not exist in DB"
        ):
            await self.delete_user_handler.handle(requested_user_id)

    async def test_get_user_throws_exception_when_user_is_already_deleted(self) -> None:
        # Given
        requested_user_id = EntityId(EntityId.new())
        requested_user = User(
            entity_id=requested_user_id,
            email="test@zw.com",
            hashed_password="hashed password",
            personal_info=PersonalInfo("first_name", "last name"),
            user_type=UserType.RIDER,
            entity_status=EntityStatus.DELETED,
        )
        self.user_repository.get_user.return_value = requested_user

        # When - Then
        with pytest.raises(
            InvalidStatusException, match=f"Entity User with id '{requested_user_id.to_str()}' is already deleted"
        ):
            await self.delete_user_handler.handle(requested_user_id)
