from unittest import mock
from uuid import UUID

import pytest

from app.core.shared.value_object.common import EntityId
from app.core.store.application.create_store import CreateStoreHandler, CreateStoreCommand, LocationCommand
from app.core.store.domain.repository.store_repository import StoreRepository


@pytest.mark.asyncio
class TestCreateStore:
    def setup(self) -> None:
        # Mock Store repository
        self.store_repository = mock.create_autospec(StoreRepository)
        self.create_store_handler = CreateStoreHandler(
            self.store_repository,
        )

    @mock.patch.object(EntityId, "new")
    async def test_create_store_successful(self, mock_new_method) -> None:
        # Given
        uuid = UUID("d7230f3a-d5cb-45b0-aa5b-9dac181aa209")
        store_id = EntityId(uuid)

        # Expected generated id
        mock_new_method.return_value = uuid

        create_store_command = CreateStoreCommand(
            name="Store name", location=LocationCommand(0.1, 0.2), description="Store description"
        )

        # When
        response = await self.create_store_handler.handle(create_store_command)

        # Then
        assert response == store_id
        self.store_repository.create_store.assert_called_once()
