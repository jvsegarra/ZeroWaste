from unittest import mock
from uuid import UUID

import pytest
from pydantic import EmailStr

from app.core.shared.value_object.common import EntityId
from app.core.user.application.signup_user import SignupUserHandler, SignupUserCommand, PersonalInfoCommand
from app.core.user.domain.repository.user_repository import UserRepository
from app.core.user.domain.value_object.user_value_object import UserType


@pytest.mark.asyncio
class TestSignupUser:
    def setup(self) -> None:
        # Mock User repository
        self.user_repository = mock.create_autospec(UserRepository)
        self.signup_user_handler = SignupUserHandler(
            self.user_repository,
        )

    @mock.patch.object(EntityId, "new")
    async def test_signup_user_successful(self, mock_new_method) -> None:
        # Given
        uuid = UUID("d7230f3a-d5cb-45b0-aa5b-9dac181aa209")
        user_id = EntityId(uuid)

        # Expected generated id
        mock_new_method.return_value = uuid

        signup_user_command = SignupUserCommand(
            email=EmailStr("test@zw.com"),
            password="test",
            personal_info=PersonalInfoCommand("first name", "last name"),
            user_type=UserType.RIDER,
        )

        # When
        response = await self.signup_user_handler.handle(signup_user_command)

        # Then
        assert response == user_id
        self.user_repository.signup_user.assert_called_once()
