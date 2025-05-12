from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field

import sqlalchemy
from src.api import auth
from src import database as db
from datetime import date

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/{class_id}/book", status_code=status.HTTP_204_NO_CONTENT)
def book_class(class_id: int, username: str):
    """
    Book a class for a user
    """

    with db.engine.begin() as connection:
        # check if the user exists
        user = connection.execute(
            sqlalchemy.text(
                """
                SELECT user_id FROM users 
                WHERE username = :username
                """
                ),
            {"username": username}
        ).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_id = user.user_id

        # check if class exists
        gym_class = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM classes 
                WHERE class_id = :class_id
                """
                ),
            {"class_id": class_id}
        ).first()

        if gym_class is None:
            raise HTTPException(status_code=404, detail="Class not found")

        # check if user already booked
        existing_booking = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 FROM bookings 
                WHERE user_id = :user_id AND class_id = :class_id
                """
                ),
            {"user_id": user_id, "class_id": class_id}
        ).first()

        if existing_booking:
            raise HTTPException(status_code=400, detail="User already booked this class")

        # insert booking
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO bookings (user_id, class_id)
                VALUES (:user_id, :class_id)
                """
                ),
            {"user_id": user_id, "class_id": class_id}
        )

@router.get("{username}/bookings")
def get_bookings(username: str):
    """
    Get all class bookings for a user
    """
    with db.engine.begin() as connection:
        # get user_id
        user = connection.execute(
            sqlalchemy.text(
                """
                SELECT user_id FROM users WHERE username = :username
                """
                ),
            {"username": username}
        ).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_id = user.user_id

        # get all bookings
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT c.class_id, c.class_name, c.day, c.start_time, c.end_time, c.instructor, c.room_number
                FROM bookings b
                JOIN classes c ON b.class_id = c.class_id
                WHERE b.user_id = :user_id
                """
            ),
            {"user_id": user_id}
        )

        bookings = [{"class_id": row.class_id,
            "class_name": row.class_name,
            "day": str(row.day),
            "start_time": row.start_time,
            "end_time": row.end_time,
            "instructor": row.instructor,
            "room_number": row.room_number
            } for row in result]

    return {"username": username, "bookings": bookings}
