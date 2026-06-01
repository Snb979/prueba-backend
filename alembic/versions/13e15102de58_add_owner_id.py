"""add owner id

Revision ID: 13e15102de58
Revises: 1b45a0cf3503
Create Date: 2026-05-29 03:09:56.029388

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '13e15102de58'
down_revision: Union[str, Sequence[str], None] = '1b45a0cf3503'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = {column["name"] for column in inspector.get_columns("vehicles")}
    if "owner_id" not in columns:
        op.add_column("vehicles", sa.Column("owner_id", sa.Integer(), nullable=True))

    foreign_keys = inspector.get_foreign_keys("vehicles")
    has_owner_fk = any(
        fk.get("referred_table") == "users"
        and fk.get("constrained_columns") == ["owner_id"]
        and fk.get("referred_columns") == ["id"]
        for fk in foreign_keys
    )
    if not has_owner_fk:
        op.create_foreign_key(
            "fk_vehicles_owner_id_users",
            "vehicles",
            "users",
            ["owner_id"],
            ["id"],
        )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = inspect(bind)

    for fk in inspector.get_foreign_keys("vehicles"):
        if fk.get("constrained_columns") == ["owner_id"] and fk.get("name"):
            op.drop_constraint(fk["name"], "vehicles", type_="foreignkey")
            break

    columns = {column["name"] for column in inspector.get_columns("vehicles")}
    if "owner_id" in columns:
        op.drop_column("vehicles", "owner_id")
