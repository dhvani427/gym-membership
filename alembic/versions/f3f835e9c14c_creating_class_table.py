"""creating class table

Revision ID: f3f835e9c14c
Revises: a058b1ef2516
Create Date: 2025-05-11 17:59:48.627418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3f835e9c14c'
down_revision: Union[str, None] = 'a058b1ef2516'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("room_id", sa.Integer, primary_key=True),
        sa.Column("number", sa.Integer, nullable=False, unique=True),
        sa.Column("capacity", sa.Integer, nullable=False),
        sa.Column("type", sa.String, nullable=False),
    )
    
    op.create_table(
        "classes",
        sa.Column("class_id", sa.Integer, primary_key=True),
        sa.Column("class_name", sa.String, nullable=False),
        sa.Column("type", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("day", sa.Date, nullable=False),
        sa.Column("capacity", sa.Integer, nullable=False),
        sa.Column("start_time", sa.String, nullable=False),
        sa.Column("end_time", sa.String, nullable=False),
        sa.Column("instructor", sa.String, nullable=False),
        sa.Column("room_id", sa.Integer, sa.ForeignKey("rooms.room_id"), nullable=False),
    )

    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("rooms")
    op.drop_table("classes")
