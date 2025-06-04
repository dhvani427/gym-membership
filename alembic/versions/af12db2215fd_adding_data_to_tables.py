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

    op.execute("""
        INSERT INTO users (username, first_name, last_name, email, date_of_birth, password, membership_plan) VALUES
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
    ( 'Weight Training', 'Weight', 'Strength training session', '2025-06-17', 30, '10:00:00', '11:30:00', 'David Wilson', 3),
    ('Pilates Basics', 'Pilates', 'Introduction to Pilates', '2025-06-18', 20, '11:00:00', '12:00:00', 'Anna Lee', 4),
    ('Advanced Pilates', 'Pilates', 'Challenging Pilates routine', '2025-06-19', 30, '12:00:00', '13:00:00', 'Evan Davis', 5);
    """)
    
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
    op.execute("DELETE FROM history")
    op.execute("DELETE FROM waitlist")
    op.execute("DELETE FROM bookings")
    op.execute("DELETE FROM classes")
    op.execute("DELETE FROM users")
    op.execute("DELETE FROM rooms")
    op.execute("DELETE FROM membership")
