"""exercises table

Revision ID: 20260611_0004
Revises: 20260610_0003
Create Date: 2026-06-11
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "20260611_0004"
down_revision = "20260610_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "exercises",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("instructions", sa.Text, nullable=True),
        sa.Column("category", sa.String(50), nullable=False, server_default="strength"),
        sa.Column("muscle_groups", sa.String(500), nullable=True),
        sa.Column("equipment", sa.String(50), nullable=False, server_default="none"),
        sa.Column("is_system", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )

    op.create_index("ix_exercises_name", "exercises", ["name"])
    op.create_index("ix_exercises_is_system", "exercises", ["is_system"])
    op.create_index("ix_exercises_user_id", "exercises", ["user_id"])
    op.create_index("ix_exercises_category", "exercises", ["category"])


def downgrade() -> None:
    op.drop_index("ix_exercises_category", table_name="exercises")
    op.drop_index("ix_exercises_user_id", table_name="exercises")
    op.drop_index("ix_exercises_is_system", table_name="exercises")
    op.drop_index("ix_exercises_name", table_name="exercises")
    op.drop_table("exercises")
