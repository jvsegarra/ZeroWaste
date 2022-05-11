"""init_users

Revision ID: 891d70b870f3
Revises: 4e590052c275
Create Date: 2022-05-11 10:44:15.827634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.dialects import postgresql

from app.core.shared.value_object.common import EntityStatus

revision = "891d70b870f3"
down_revision = "4e590052c275"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column("email", sa.String(100), nullable=False, index=True, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("user_type", sa.String(50), nullable=False),
        sa.Column("entity_status", sa.String(50), nullable=False, server_default=EntityStatus.ACTIVE.value),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table("users")
