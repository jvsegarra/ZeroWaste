from typing import Optional

from databases.backends.postgres import Record

from app.core.shared.value_object.common import EntityId, EntityStatus
from app.core.user.domain.entity.user import User
from app.core.user.domain.value_object.user_value_object import PersonalInfo, UserType
from config.database import database


class UserRepositoryPostgres:
    async def signup_user(self, user: User):
        query = """
        INSERT INTO users (id, email, hashed_password, first_name, last_name, user_type)
        VALUES (:id, :email, :hashed_password, :first_name, :last_name, :user_type)
        """

        await database.execute(
            query=query,
            values=self._map_to_dict(user),
        )

    async def get_user(self, user_id: EntityId) -> Optional[User]:
        query = "SELECT * FROM users WHERE id = :id"

        user_db = await database.fetch_one(query=query, values={"id": user_id.to_str()})

        if not user_db:
            return None

        return self._map_to_user_entity(user_db)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE email = :email"

        user_db = await database.fetch_one(query=query, values={"email": email})

        if not user_db:
            return None

        return self._map_to_user_entity(user_db)

    async def delete_user(self, user_id: EntityId):
        query = f"UPDATE users set deleted_at = now(), entity_status = :entity_status WHERE id = :id"

        await database.execute(
            query=query,
            values={
                "entity_status": EntityStatus.DELETED.value,
                "id": user_id.to_str(),
            },
        )

    def _map_to_dict(self, user: User) -> dict:
        return {
            "id": user.id.to_str(),
            "email": user.email,
            "hashed_password": user.hashed_password,
            "first_name": user.personal_info.first_name,
            "last_name": user.personal_info.last_name,
            "user_type": user.user_type.value,
        }

    def _map_to_user_entity(self, user_db: Record) -> User:
        return User(
            entity_id=EntityId(user_db["id"]),
            entity_status=EntityStatus(user_db["entity_status"]),
            email=user_db["email"],
            hashed_password=user_db["hashed_password"],
            personal_info=PersonalInfo(user_db["first_name"], user_db["last_name"]),
            user_type=UserType(user_db["user_type"]),
        )
