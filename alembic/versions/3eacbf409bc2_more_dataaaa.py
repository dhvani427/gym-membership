"""more dataaaa

Revision ID: 3eacbf409bc2
Revises: 898f0a111bf3
Create Date: 2025-06-04 00:38:10.030409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eacbf409bc2'
down_revision: Union[str, None] = '898f0a111bf3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    INSERT INTO bookings (class_id, user_id) VALUES
    (1, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (3, 5),
    (4, 6),
    (5, 7),
    (2, 7),
    (3, 7),
    (3, 7),
    (4, 7),
    (6, 8),
    (7, 9),
    (8, 10);

    """)

    op.execute("""
            INSERT INTO history (check_in_date, check_in_time, user_id) VALUES
            ('2025-06-01', '08:15:00', 1),
            ('2025-06-01', '09:00:00', 2),
            ('2025-06-02', '10:30:00', 3),
            ('2025-06-02', '07:45:00', 4),
            ('2025-06-03', '12:00:00', 5),
            ('2025-06-03', '15:30:00', 6),
            ('2025-06-03', '17:00:00', 7),
            ('2025-06-03', '18:45:00', 8),
            ('2025-06-02', '08:30:00', 9),
            ('2025-06-01', '14:00:00', 10)
        """)

def downgrade() -> None:
    """Downgrade schema."""
    pass
