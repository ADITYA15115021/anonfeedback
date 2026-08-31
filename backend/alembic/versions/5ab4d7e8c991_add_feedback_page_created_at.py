"""add feedback page creation timestamp

Revision ID: 5ab4d7e8c991
Revises: 3d9e6b1a7f22
Create Date: 2026-08-31
"""

from alembic import op
import sqlalchemy as sa


revision = "5ab4d7e8c991"
down_revision = "3d9e6b1a7f22"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "feedback_pages",
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_column("feedback_pages", "created_at")
