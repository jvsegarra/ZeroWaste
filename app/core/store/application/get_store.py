from app.core.shared.exception.base_exceptions import EntityNotFoundException, InvalidStatusException
from app.core.shared.value_object.common import EntityId
from app.core.store.domain.entity.store import Store
from app.core.store.domain.repository.store_repository import StoreRepository


class GetStoreHandler:
    store_repository: StoreRepository

    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    async def handle(self, store_id: EntityId) -> Store:
        store = await self.store_repository.get_store(store_id)

        if not store:
            raise EntityNotFoundException(f"Store id '{store_id.to_str()}' does not exist in DB")

        return store
