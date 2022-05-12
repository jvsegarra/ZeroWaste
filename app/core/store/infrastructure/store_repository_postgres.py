from typing import Optional

from databases.backends.postgres import Record

from app.core.shared.value_object.common import EntityId, EntityStatus
from app.core.store.domain.entity.store import Store
from app.core.store.domain.value_object.store_value_object import Location
from config.database import database


class StoreRepositoryPostgres:
    async def create_store(self, store: Store):
        query = """
        INSERT INTO stores (id, name, location_longitude, location_latitude, description)
        VALUES (:id, :name, :location_longitude, :location_latitude, :description)
        """

        await database.execute(
            query=query,
            values=self._map_to_dict(store),
        )

    async def get_store(self, store_id: EntityId) -> Optional[Store]:
        query = "SELECT * FROM stores WHERE id = :id"

        store_db = await database.fetch_one(query=query, values={"id": store_id.to_str()})

        if not store_db:
            return None

        return self._map_to_store_entity(store_db)

    async def delete_store(self, store_id: EntityId):
        query = f"UPDATE stores set deleted_at = now(), entity_status = :entity_status WHERE id = :id"

        await database.execute(
            query=query,
            values={
                "entity_status": EntityStatus.DELETED.value,
                "id": store_id.to_str(),
            },
        )

    def _map_to_dict(self, store: Store) -> dict:
        return {
            "id": store.id.to_str(),
            "name": store.name,
            "location_longitude": store.location.longitude,
            "location_latitude": store.location.latitude,
            "description": store.description,
        }

    def _map_to_store_entity(self, store_db: Record) -> Store:
        return Store(
            entity_id=EntityId(store_db["id"]),
            entity_status=EntityStatus(store_db["entity_status"]),
            name=store_db["name"],
            location=Location(store_db["location_longitude"], store_db["location_latitude"]),
            description=store_db["description"],
        )
