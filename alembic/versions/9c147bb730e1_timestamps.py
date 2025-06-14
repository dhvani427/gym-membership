"""timestamps

Revision ID: 9c147bb730e1
Revises: e8147e1c2659
Create Date: 2025-05-30 21:48:54.894022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text, func



# revision identifiers, used by Alembic.
revision: str = '9c147bb730e1'
down_revision: Union[str, None] = 'e8147e1c2659'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # Change column types with USING to avoid cast errors
    op.alter_column(
        "history",
        "check_in_date",
        type_=sa.Date(),
        existing_type=sa.String,
        postgresql_using="check_in_date::date"
    )
    op.alter_column(
        "history",
        "check_in_time",
        type_=sa.Time(),
        existing_type=sa.String,
        postgresql_using="check_in_time::time"
    )
    # Then your UPDATE statement if needed
    conn = op.get_bind()
    conn.execute(text("""
        UPDATE history
        SET check_in_date = CURRENT_DATE,
            check_in_time = CURRENT_TIME::time
    """))

    op.alter_column(
        "classes",
        "day",
        type_=sa.Date(),
        existing_type=sa.String,
        postgresql_using="day::date"
    )
    op.alter_column(
        "classes",
        "start_time",
        type_=sa.Time(),
        existing_type=sa.String,
        postgresql_using="start_time::time"
    )
    op.alter_column(
        "classes",
        "end_time",
        type_=sa.Time(),
        existing_type=sa.String,
        postgresql_using="end_time::time"
    )
    # Your UPDATE for classes
    conn.execute(text("""
        UPDATE classes
        SET day = CURRENT_DATE,
            start_time = CURRENT_TIME::time,
            end_time = CURRENT_TIME::time
    """))



def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("history", "check_in_date", type_=sa.String(), existing_type=sa.Date)
    op.alter_column("history", "check_in_time", type_=sa.String(), existing_type=sa.Time)

    # Optionally set values to string versions of date/time
    conn = op.get_bind()
    conn.execute(text("""
        UPDATE history
        SET check_in_date = TO_CHAR(CURRENT_DATE, 'YYYY-MM-DD'),
            check_in_time = TO_CHAR(CURRENT_TIME::time, 'HH24:MI:SS')
    """))

    # Revert column types in 'classes'
    op.alter_column("classes", "day", type_=sa.String(), existing_type=sa.Date)
    op.alter_column("classes", "start_time", type_=sa.String(), existing_type=sa.Time)
    op.alter_column("classes", "end_time", type_=sa.String(), existing_type=sa.Time)

    conn.execute(text("""
        UPDATE classes
        SET day = TO_CHAR(CURRENT_DATE, 'YYYY-MM-DD'),
            start_time = TO_CHAR(CURRENT_TIME::time, 'HH24:MI:SS'),
            end_time = TO_CHAR(CURRENT_TIME::time, 'HH24:MI:SS')
    """))
