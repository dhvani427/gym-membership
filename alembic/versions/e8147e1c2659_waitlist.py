"""waitlist

Revision ID: e8147e1c2659
Revises: 78d6fdff9161
Create Date: 2025-05-22 17:19:06.248331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8147e1c2659'
down_revision: Union[str, None] = '78d6fdff9161'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "waitlist",
        sa.Column("class_id", sa.Integer, sa.ForeignKey("classes.class_id"), primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.user_id"), primary_key=True),
        sa.Column("waitlist_position", sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint("class_id", "user_id")
    )


def downgrade() -> None:
    """Downgrade schema."""
    #op.drop_table("waitlist")
    pass
