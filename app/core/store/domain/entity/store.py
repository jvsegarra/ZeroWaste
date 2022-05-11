from app.core.shared.entity.base_entity import BaseEntity
from app.core.shared.value_object.common import EntityId, EntityStatus
from app.core.store.domain.value_object.store_value_object import Location


class Store(BaseEntity):
    name: str
    location: Location
    description: str

    def __init__(
        self,
        entity_id: EntityId,
        name: str,
        location: Location,
        entity_status: EntityStatus = EntityStatus.ACTIVE,
        description: str = None,
    ):
        super().__init__(entity_id, entity_status=entity_status)
        self.name = name
        self.location = location
        self.description = description
