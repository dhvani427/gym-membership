"""Adding data to tables

Revision ID: af12db2215fd
Revises: 9c147bb730e1
Create Date: 2025-06-03 20:51:43.493025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af12db2215fd'
down_revision: Union[str, None] = '9c147bb730e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO membership (membership_plan, cost, max_classes) VALUES
        ('Basic', 30, 5),
        ('Standard', 50, 10),
        ('Elite', 80, 20)
    """)

    op.execute("""
        INSERT INTO rooms (room_number, capacity, type) VALUES
        ( 1, 15, 'Yoga' ),
        ( 2, 10, 'Cardio' ),
        ( 3, 30, 'Weight' ),
        ( 4, 20, 'Pilates' ),
        ( 5, 30, 'Pilates' ),
        ( 6, 10, 'Weight' ),
        ( 7, 5, 'Stretch' ),
        ( 8, 5, 'Yoga' ),
        ( 9, 10, 'Cardio' ),
        ( 10, 30, 'Weight' )
    """)

    


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM history")
    op.execute("DELETE FROM waitlist")
    op.execute("DELETE FROM bookings")
    op.execute("DELETE FROM classes")
    op.execute("DELETE FROM users")
    op.execute("DELETE FROM rooms")
    op.execute("DELETE FROM membership")
