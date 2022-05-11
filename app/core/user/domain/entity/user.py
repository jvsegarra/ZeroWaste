from app.core.shared.value_object.common import EntityId, EntityStatus
from app.core.user.domain.value_object.user_value_object import PersonalInfo, UserType
from app.core.shared.entity.base_entity import BaseEntity


class User(BaseEntity):
    email: str
    hashed_password: str
    personal_info: PersonalInfo
    user_type: UserType

    def __init__(
        self,
        entity_id: EntityId,
        email: str,
        hashed_password: str,
        personal_info: PersonalInfo,
        user_type: UserType,
        entity_status: EntityStatus = EntityStatus.ACTIVE,
    ):
        super().__init__(entity_id, entity_status)
        self.email = email
        self.hashed_password = hashed_password
        self.personal_info = personal_info
        self.user_type = user_type
