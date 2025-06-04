"""more data

Revision ID: 898f0a111bf3
Revises: af12db2215fd
Create Date: 2025-06-03 23:45:59.373797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '898f0a111bf3'
down_revision: Union[str, None] = 'af12db2215fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO users (username, first_name, last_name, email, date_of_birth, password, membership) VALUES
        ('alice1', 'Alice', 'Smith', 'alice@example.com', '2000-01-01', 'pw123', 1),
        ('bob22', 'Bob', 'Jones', 'bob@example.com', '1999-05-10', 'pw123', 2),
        ('charlie3', 'Charlie', 'Kim', 'charlie@example.com', '2001-07-15', 'pw123', 2),
        ('diana4', 'Diana', 'Singh', 'diana@example.com', '2002-08-18', 'pw123', 3),
        ('eric5', 'Eric', 'Zhao', 'eric@example.com', '2003-09-20', 'pw123', 1),
        ('fiona6', 'Fiona', 'Nguyen', 'fiona@example.com', '2000-02-25', 'pw123', 1),
        ('george7', 'George', 'Lee', 'george@example.com', '1998-12-30', 'pw123', 2),
        ('hannah8', 'Hannah', 'Brown', 'hannah@example.com', '2001-04-04', 'pw123', 3),
        ('ian9', 'Ian', 'Wilson', 'ian@example.com', '1997-06-06', 'pw123', 1),
        ('jane10', 'Jane', 'Kaur', 'jane@example.com', '2003-03-03', 'pw123', 2)
    """)

    op.execute("""
    INSERT INTO classes (class_name, class_type, description, day, capacity, start_time, end_time, instructor, room_number) VALUES
    ('Morning Yoga', 'Yoga', 'Start your day with calming yoga', '2025-06-04', 15, '08:00:00', '09:00:00', 'John Smith', 1),
    ('Cardio Blast', 'Cardio', 'High-intensity cardio workout', '2025-06-05', 10, '09:00:00', '10:00:00', 'Jane Doe', 2),
    ('Weight Training', 'Weight', 'Strength training session', '2025-06-06', 30, '10:00:00', '11:30:00', 'David Wilson', 3),
    ('Pilates Basics', 'Pilates', 'Introduction to Pilates', '2025-06-07', 20, '11:00:00', '12:00:00', 'Anna Lee', 4),
    ('Advanced Pilates', 'Pilates', 'Challenging Pilates routine', '2025-06-08', 30, '12:00:00', '13:00:00', 'Evan Davis', 5),
    ('Weight Circuit', 'Weight', 'Circuit training with weights', '2025-06-09', 10, '13:00:00', '14:00:00', 'Sarah Miller', 6),
    ('Stretch & Relax', 'Stretch', 'Full body stretching', '2025-06-10', 5, '14:00:00', '14:45:00', 'Grace Hall', 7),
    ('Evening Yoga', 'Yoga', 'Relaxing yoga to end the day', '2025-06-11', 5, '18:00:00', '19:00:00', 'John Smith', 8),
    ('Cardio Kickboxing', 'Cardio', 'Kickboxing for cardio', '2025-06-12', 10, '17:00:00', '18:00:00', 'Tom Clark', 9),
    ('Power Weightlifting', 'Weight', 'Intense weightlifting', '2025-06-13', 30, '15:00:00', '16:30:00', 'Chris Johnson', 10),
    ('Morning Yoga', 'Yoga', 'Start your day with calming yoga', '2025-06-15', 15, '08:00:00', '09:00:00', 'John Smith', 1),
    ('Cardio Blast', 'Cardio', 'High-intensity cardio workout', '2025-06-16', 10, '09:00:00', '10:00:00', 'Jane Doe', 2),
    ('Weight Training', 'Weight', 'Strength training session', '2025-06-17', 30, '10:00:00', '11:30:00', 'David Wilson', 3),
    ('Pilates Basics', 'Pilates', 'Introduction to Pilates', '2025-06-18', 20, '11:00:00', '12:00:00', 'Anna Lee', 4),
    ('Advanced Pilates', 'Pilates', 'Challenging Pilates routine', '2025-06-19', 30, '12:00:00', '13:00:00', 'Evan Davis', 5);
""")
    
    


def downgrade() -> None:
    """Downgrade schema."""
    pass
