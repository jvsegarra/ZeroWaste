from http import HTTPStatus

from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.core.shared.value_object.common import EntityId
from app.core.store.application.create_store import CreateStoreCommand, LocationCommand
from app.di.store import get_create_store_handler, get_get_store_handler, get_delete_store_handler
from app.rest_api.store.dto import StoreApiDto, LocationApiDto

store_router = APIRouter(
    prefix="/stores",
    tags=["stores"],
)


@store_router.post("/", status_code=HTTPStatus.CREATED)
async def create_store(store_request: StoreApiDto, create_store_handler=Depends(get_create_store_handler)):
    store_id = await create_store_handler.handle(
        CreateStoreCommand(
            name=store_request.name,
            description=store_request.description,
            location=LocationCommand(store_request.location.longitude, store_request.location.latitude),
        )
    )

    return {"store_id": store_id.to_str()}


@store_router.get("/{store_id}", response_model=StoreApiDto)
async def get_store(store_id, get_store_handler=Depends(get_get_store_handler)):
    store = await get_store_handler.handle(EntityId.from_str(store_id))

    return StoreApiDto(
        name=store.name,
        location=LocationApiDto.from_location(store.location),
        description=store.description,
    )


@store_router.delete("/{store_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_store(store_id, delete_store_handler=Depends(get_delete_store_handler)):
    await delete_store_handler.handle(EntityId.from_str(store_id))

    return Response(status_code=HTTPStatus.NO_CONTENT)
