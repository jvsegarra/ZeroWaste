from unittest import mock

import pytest

from app.core.shared.exception.base_exceptions import EntityNotFoundException
from app.core.shared.value_object.common import EntityId
from app.core.store.application.get_store import GetStoreHandler
from app.core.store.domain.entity.store import Store
from app.core.store.domain.repository.store_repository import StoreRepository
from app.core.store.domain.value_object.location import Location


@pytest.mark.asyncio
class TestGetstore:
    def setup(self) -> None:
        self.store_repository = mock.create_autospec(StoreRepository)
        self.get_store_handler = GetStoreHandler(self.store_repository)

    async def test_get_store_returns_store_successfully(self) -> None:
        # Given
        requested_store_id = EntityId(EntityId.new())
        requested_store = Store(
            entity_id=requested_store_id,
            name="Store test",
            location=Location(longitude=0.1, latitude=0.2),
        )
        self.store_repository.get_store.return_value = requested_store

        # When
        response = await self.get_store_handler.handle(requested_store_id)

        # Then
        assert response == requested_store

    async def test_get_store_throws_exception_when_store_does_not_exist(self) -> None:
        # Given
        requested_store_id = EntityId(EntityId.new())
        self.store_repository.get_store.return_value = None

        # When - Then
        with pytest.raises(
            EntityNotFoundException, match=f"Store id '{requested_store_id.to_str()}' does not exist in DB"
        ):
            await self.get_store_handler.handle(requested_store_id)
