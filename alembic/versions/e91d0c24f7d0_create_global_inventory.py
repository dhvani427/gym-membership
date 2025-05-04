"""create global inventory

Revision ID: e91d0c24f7d0
Revises:
Create Date: 2025-03-30 11:23:36.782933

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e91d0c24f7d0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, nullable=False, unique=True),
        sa.Column("first_name", sa.String, nullable=False),
        sa.Column("last_name", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("date_of_birth", sa.Date, nullable=False),
        sa.Column("password", sa.String, nullable=False),
    )

def downgrade():
    op.drop_table("users")
