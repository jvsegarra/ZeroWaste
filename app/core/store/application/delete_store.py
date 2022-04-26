from app.core.shared.exception.base_exceptions import EntityNotFoundException, InvalidStatusException
from app.core.shared.value_object.common import EntityId
from app.core.store.domain.repository.store_repository import StoreRepository


class DeleteStoreHandler:
    store_repository: StoreRepository

    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    async def handle(self, store_id: EntityId):
        store = await self.store_repository.get_store(store_id)

        if not store:
            raise EntityNotFoundException(f"Store id '{store_id.to_str()}' does not exist in DB")

        if store.is_deleted:
            raise InvalidStatusException(f"Entity Store with id '{store_id.to_str()}' is already deleted")

        await self.store_repository.delete_store(store.id)
