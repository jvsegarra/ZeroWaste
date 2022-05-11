from app.core.store.application.create_store import CreateStoreHandler
from app.core.store.application.delete_store import DeleteStoreHandler
from app.core.store.application.get_store import GetStoreHandler
from app.core.store.infrastructure.store_repository_postgres import StoreRepositoryPostgres


async def get_create_store_handler():
    handler = CreateStoreHandler(StoreRepositoryPostgres())
    yield handler


async def get_get_store_handler():
    handler = GetStoreHandler(StoreRepositoryPostgres())
    yield handler


async def get_delete_store_handler():
    handler = DeleteStoreHandler(StoreRepositoryPostgres())
    yield handler
