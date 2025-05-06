"""membership table

Revision ID: a058b1ef2516
Revises: e91d0c24f7d0
Create Date: 2025-05-05 17:22:04.017856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a058b1ef2516'
down_revision: Union[str, None] = 'e91d0c24f7d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "membership",
        sa.Column("membership_id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False, unique=True),
        sa.Column("cost", sa.Integer, nullable=False),
        sa.Column("max_classes", sa.Integer, nullable=False),
    )

    op.add_column(
        "users",
        sa.Column("membership_plan", sa.Integer, sa.ForeignKey("membership.membership_id"), nullable=True),
    )
    

def downgrade():
    op.drop_table("membership")

    op.drop_column("users", "membership_plan")