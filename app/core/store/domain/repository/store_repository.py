from typing import Protocol

from app.core.shared.value_object.common import EntityId
from app.core.store.domain.entity.store import Store


class StoreRepository(Protocol):
    async def create_store(self, store: Store):
        """Persists a Store in DB"""

    async def get_store(self, store_id: EntityId) -> Store:
        """Fetches a store from DB by its Id"""

    async def delete_store(self, store_id: EntityId):
        """Deletes a store from DB by its Id"""
