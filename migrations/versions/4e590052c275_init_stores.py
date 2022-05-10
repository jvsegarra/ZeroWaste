"""init_stores

Revision ID: 4e590052c275
Revises: 
Create Date: 2022-05-05 14:22:59.703462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.dialects import postgresql

from app.core.shared.value_object.common import EntityStatus

revision = "4e590052c275"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "stores",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("location_longitude", sa.Float, nullable=False),
        sa.Column("location_latitude", sa.Float, nullable=False),
        sa.Column("description", sa.Unicode(255)),
        sa.Column("entity_status", sa.String(50), nullable=False, server_default=EntityStatus.ACTIVE.value),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table("stores")
