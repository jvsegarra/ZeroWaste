from enum import Enum
from uuid import UUID, uuid4

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class EntityId:
    id: UUID

    @staticmethod
    def new() -> UUID:
        return uuid4()

    @staticmethod
    def from_str(string: str) -> "EntityId":
        return EntityId(id=UUID(string))

    def to_str(self) -> str:
        return str(self.id)


class EntityStatus(Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
