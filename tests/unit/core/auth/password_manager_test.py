import pytest
from unittest import mock

from app.core.auth.password_manager import PasswordManager


class TestPasswordManager:
    @mock.patch("app.core.auth.password_manager.bcrypt")
    def test_hash_password_returns_result_from_bcrypt(self, bcrypt_mock):
        # Given
        str_to_encrypt = "test"
        bcrypt_mock.hash.return_value = "hashed string"

        # When
        result = PasswordManager.hash_password(str_to_encrypt)

        # Then
        assert result == "hashed string"

    @mock.patch("app.core.auth.password_manager.bcrypt")
    @pytest.mark.parametrize("bcrypt_result", [True, False])
    def test_verify_returns_result_from_bcrypt(self, bcrypt_mock, bcrypt_result):
        # Given
        password_to_verify = "test"
        hashed_password = "adfasdfpiouoiu"
        bcrypt_mock.verify.return_value = bcrypt_result

        # When
        result = PasswordManager.verify_password(password_to_verify, hashed_password)

        # Then
        assert result == bcrypt_result
