from unittest import mock

import pytest

from app.core.auth.auth_manager import AuthManager
from app.core.auth.password_manager import PasswordManager
from app.core.shared.exception.base_exceptions import AuthException
from app.core.shared.value_object.common import EntityId
from app.core.user.domain.entity.user import User
from app.core.user.domain.repository.user_repository import UserRepository
from app.core.user.domain.value_object.user_value_object import PersonalInfo, UserType


@pytest.mark.asyncio
class TestAuthManager:
    def setup(self) -> None:
        # Mock User repository
        self.user_repository = mock.create_autospec(UserRepository)
        self.auth_manager = AuthManager(
            self.user_repository,
        )

    @mock.patch.object(PasswordManager, "verify_password")
    async def test_authenticate_returns_user_successfully(self, verify_password_mock):
        # Given
        requested_user = User(
            entity_id=EntityId(EntityId.new()),
            email="test@zw.com",
            hashed_password="hashed password",
            personal_info=PersonalInfo("first_name", "last name"),
            user_type=UserType.RIDER,
        )
        self.user_repository.get_user_by_email.return_value = requested_user
        verify_password_mock.return_value = True

        # When
        result = await self.auth_manager.authenticate_user("test@zw.com", "test password")

        # then
        assert result == requested_user

    async def test_exception_thrown_when_user_is_not_found_by_credentials(self):
        # Given
        requested_user = User(
            entity_id=EntityId(EntityId.new()),
            email="test@zw.com",
            hashed_password="hashed password",
            personal_info=PersonalInfo("first_name", "last name"),
            user_type=UserType.RIDER,
        )
        self.user_repository.get_user_by_email.return_value = None

        # When - Then
        with pytest.raises(AuthException, match=f"Incorrect username or password"):
            await self.auth_manager.authenticate_user("test@zw.com", "test password")

    @mock.patch.object(PasswordManager, "verify_password")
    async def test_exception_thrown_when_verification_fails(self, verify_password_mock):
        # Given
        requested_user = User(
            entity_id=EntityId(EntityId.new()),
            email="test@zw.com",
            hashed_password="hashed password",
            personal_info=PersonalInfo("first_name", "last name"),
            user_type=UserType.RIDER,
        )
        self.user_repository.get_user_by_email.return_value = requested_user
        verify_password_mock.return_value = False

        # When - Then
        with pytest.raises(AuthException, match=f"Incorrect username or password"):
            await self.auth_manager.authenticate_user("test@zw.com", "test password")

    @mock.patch("app.core.auth.auth_manager.jwt.decode")
    async def test_get_current_user_returns_user_successfully(self, jwt_decode_mock):
        # Given
        requested_user = User(
            entity_id=EntityId(EntityId.new()),
            email="test@zw.com",
            hashed_password="hashed password",
            personal_info=PersonalInfo("first_name", "last name"),
            user_type=UserType.RIDER,
        )
        self.user_repository.get_user_by_email.return_value = requested_user
        jwt_decode_mock.return_value = {
            "sub": "test@zw.com",
        }

        # When
        result = await self.auth_manager.get_current_user("user token")

        # Then
        assert result == requested_user

    @mock.patch("app.core.auth.auth_manager.jwt.decode")
    async def test_exception_thrown_when_email_is_missing_in_credentials(self, jwt_decode_mock):
        # Given
        requested_user = User(
            entity_id=EntityId(EntityId.new()),
            email="test@zw.com",
            hashed_password="hashed password",
            personal_info=PersonalInfo("first_name", "last name"),
            user_type=UserType.RIDER,
        )
        self.user_repository.get_user_by_email.return_value = requested_user
        jwt_decode_mock.return_value = {"iat": "some timestamp"}

        # When - Then
        with pytest.raises(AuthException, match=f"Could not validate credentials"):
            await self.auth_manager.get_current_user("user token")

    @mock.patch("app.core.auth.auth_manager.jwt.decode")
    async def test_exception_thrown_when_user_for_token_is_not_in_db(self, jwt_decode_mock):
        # Given
        requested_user = User(
            entity_id=EntityId(EntityId.new()),
            email="test@zw.com",
            hashed_password="hashed password",
            personal_info=PersonalInfo("first_name", "last name"),
            user_type=UserType.RIDER,
        )
        self.user_repository.get_user_by_email.return_value = None
        jwt_decode_mock.return_value = {
            "sub": "test@zw.com",
        }

        # When - Then
        with pytest.raises(AuthException, match=f"Could not validate credentials"):
            await self.auth_manager.get_current_user("user token")
