"""history and bookings tables

Revision ID: 78d6fdff9161
Revises: f3f835e9c14c
Create Date: 2025-05-12 10:25:40.245062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78d6fdff9161'
down_revision: Union[str, None] = 'f3f835e9c14c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "history",
        sa.Column("history_id", sa.Integer, primary_key=True),
        sa.Column("check_in_date", sa.String, nullable=False),
        sa.Column("check_in_time", sa.String, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.user_id"), nullable=False)
    )

    op.create_table(
        "bookings",
        sa.Column("booking_id", sa.Integer, primary_key=True),
        sa.Column("class_id", sa.Integer, sa.ForeignKey("classes.class_id"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.user_id"), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("history")
    op.drop_table("bookings")
