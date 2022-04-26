from fastapi import APIRouter
from http import HTTPStatus

from app.core.store.application.create_store import CreateStoreHandler, CreateStoreCommand, LocationCommand
from app.core.store.infrastructure.store_repository_postgres import StoreRepositoryPostgres
from app.rest_api.store.api_dto import StoreApiDto, LocationApiDto
from app.core.store.application.delete_store import DeleteStoreHandler
from app.core.shared.value_object.common import EntityId
from app.core.store.application.get_store import GetStoreHandler

router = APIRouter(
    prefix="/stores",
    tags=["stores"],
)


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_store(store_request: StoreApiDto):
    create_store_handler = CreateStoreHandler(StoreRepositoryPostgres())
    store_id = await create_store_handler.handle(
        CreateStoreCommand(
            name=store_request.name,
            description=store_request.description,
            location=LocationCommand(store_request.location.longitude, store_request.location.latitude),
        )
    )

    return {"store_id": store_id.to_str()}


@router.get("/{store_id}", response_model=StoreApiDto)
async def get_store(store_id):
    get_store_handler = GetStoreHandler(StoreRepositoryPostgres())
    store = await get_store_handler.handle(EntityId.from_str(store_id))

    return StoreApiDto(
        name=store.name,
        location=LocationApiDto.from_location(store.location),
        description=store.description,
    )


@router.delete("/{store_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_store(store_id):
    delete_store_handler = DeleteStoreHandler(StoreRepositoryPostgres())
    await delete_store_handler.handle(EntityId.from_str(store_id))
