from unittest import mock

from app.core.auth.auth_manager import TokenManager


class TestTokenManager:
    @mock.patch("app.core.auth.auth_manager.jwt.encode")
    def test_create_access_token_returns_result_from_jwt_encode(self, jwt_encode_mock):
        # Given
        jwt_encode_mock.return_value = "payload encoded"

        # When
        result = TokenManager.create_access_token("access_token_email")

        # Then
        assert result == "payload encoded"
