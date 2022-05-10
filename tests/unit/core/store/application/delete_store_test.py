from unittest import mock

import pytest

from app.core.shared.exception.base_exceptions import EntityNotFoundException, InvalidStatusException
from app.core.shared.value_object.common import EntityId, EntityStatus
from app.core.store.application.delete_store import DeleteStoreHandler
from app.core.store.domain.entity.store import Store
from app.core.store.domain.repository.store_repository import StoreRepository
from app.core.store.domain.value_object.location import Location


@pytest.mark.asyncio
class TestDeletestore:
    def setup(self) -> None:
        self.store_repository = mock.create_autospec(StoreRepository)
        self.delete_store_handler = DeleteStoreHandler(self.store_repository)

    async def test_delete_store_successfully(self) -> None:
        # Given
        requested_store_id = EntityId(EntityId.new())
        requested_store = Store(
            entity_id=requested_store_id,
            name="Store test",
            location=Location(longitude=0.1, latitude=0.2),
        )
        self.store_repository.get_store.return_value = requested_store

        # When
        await self.delete_store_handler.handle(requested_store_id)

        # Then
        self.store_repository.delete_store.assert_called_once_with(requested_store_id)

    async def test_get_store_throws_exception_when_store_does_not_exist(self) -> None:
        # Given
        requested_store_id = EntityId(EntityId.new())
        self.store_repository.get_store.return_value = None

        # When - Then
        with pytest.raises(
            EntityNotFoundException, match=f"Store id '{requested_store_id.to_str()}' does not exist in DB"
        ):
            await self.delete_store_handler.handle(requested_store_id)

    async def test_get_store_throws_exception_when_store_is_already_deleted(self) -> None:
        # Given
        requested_store_id = EntityId(EntityId.new())
        requested_store = Store(
            entity_id=requested_store_id,
            name="Store test",
            location=Location(longitude=0.1, latitude=0.2),
            entity_status=EntityStatus.DELETED,
        )
        self.store_repository.get_store.return_value = requested_store

        # When - Then
        with pytest.raises(
            InvalidStatusException, match=f"Entity Store with id '{requested_store_id.to_str()}' is already deleted"
        ):
            await self.delete_store_handler.handle(requested_store_id)
