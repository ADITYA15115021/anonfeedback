"""rename user name column to username

Revision ID: 3d9e6b1a7f22
Revises: 60650c82b8e5
Create Date: 2026-08-31
"""

from alembic import op
import sqlalchemy as sa


revision = "3d9e6b1a7f22"
down_revision = "60650c82b8e5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # batch mode keeps this migration compatible with SQLite as well as Postgres.
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "name",
            new_column_name="username",
            existing_type=sa.String(length=100),
            existing_nullable=True,
            nullable=False,
        )
        batch_op.create_unique_constraint("uq_users_username", ["username"])


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint("uq_users_username", type_="unique")
        batch_op.alter_column(
            "username",
            new_column_name="name",
            existing_type=sa.String(length=100),
            existing_nullable=False,
            nullable=True,
        )
