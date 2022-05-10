from typing import Optional
from uuid import uuid4

from pydantic.dataclasses import dataclass

from app.core.shared.value_object.common import EntityId
from app.core.store.domain.entity.store import Store
from app.core.store.domain.repository.store_repository import StoreRepository
from app.core.store.domain.value_object.location import Location


@dataclass
class LocationCommand:
    longitude: float
    latitude: float


@dataclass
class CreateStoreCommand:
    name: str
    location: LocationCommand
    description: Optional[str] = None


class CreateStoreHandler:
    store_repository: StoreRepository

    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    async def handle(self, command: CreateStoreCommand) -> EntityId:
        store = Store(
            entity_id=EntityId(EntityId.new()),
            name=command.name,
            location=Location(command.location.longitude, command.location.latitude),
            description=command.description,
        )

        await self.store_repository.create_store(store)

        return store.id
