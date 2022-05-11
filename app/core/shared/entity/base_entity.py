from datetime import datetime
from typing import Optional

from app.core.shared.value_object.common import EntityId, EntityStatus


class BaseEntity:
    id: EntityId
    entity_status: EntityStatus
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    def __init__(self, entity_id: EntityId, entity_status: EntityStatus = EntityStatus.ACTIVE):
        self.id = entity_id
        self.entity_status = entity_status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.deleted_at = None

    @property
    def is_deleted(self) -> bool:
        return self.entity_status == EntityStatus.DELETED
