from fastapi import APIRouter, Depends, status, HTTPException, Body
from pydantic import BaseModel, Field

import sqlalchemy
from src.api import auth
from src import database as db
import datetime
from typing import Optional

import time

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
    dependencies=[Depends(auth.get_api_key)],
)

class BookingRequest(BaseModel):
    class_id: int
    username: str

class BookingResponse(BaseModel):
    class_id: int
    enrollment_status: str = Field(
        default="Booking successful")

@router.post("/book", response_model=BookingResponse)
def book_class(booking: BookingRequest):
    start_time = time.time()
    class_id = booking.class_id
    username = booking.username
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
            raise HTTPException(status_code=422, detail="User not found")

        user_id = user.user_id

        # check if class exists and get capacity
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
            raise HTTPException(status_code=422, detail="Class not found")
        
        # check if user already booked the class
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

        
        # check if class is full
        class_capacity = gym_class.capacity
        booked_count = connection.execute(
            sqlalchemy.text(
                """
                SELECT COUNT(*) FROM bookings 
                WHERE class_id = :class_id
                """
                ),
            {"class_id": class_id}
        ).scalar()

        # check if class is full
        if booked_count >= class_capacity:
            return BookingResponse(
                class_id=class_id,
                enrollment_status="Class is full, please join the waitlist or choose another class"
            )

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

        return BookingResponse(
            class_id=class_id,
            enrollment_status="Booking successful"
        )

class CancelResponse(BaseModel):
    class_id: int
    cancellation_status: str
    enrolled_from_waitlist: Optional[str] = None 

@router.delete("/{class_id}/cancel", response_model=CancelResponse)
def cancel_booking(class_id: int, username: str):
    """
    Cancel a class booking for a user, and enroll first waitlist user
    """
    start_time = time.time()
    with db.engine.begin() as connection:
        # Check if user exists
        user = connection.execute(
            sqlalchemy.text("SELECT user_id FROM users WHERE username = :username"),
            {"username": username}
        ).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_id = user.user_id

        # check if booking exists
        booking = connection.execute(
            sqlalchemy.text(
                "SELECT * FROM bookings WHERE user_id = :user_id AND class_id = :class_id"
            ),
            {"user_id": user_id, "class_id": class_id}
        ).first()

        if booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")

        # delete booking
        connection.execute(
            sqlalchemy.text(
                "DELETE FROM bookings WHERE user_id = :user_id AND class_id = :class_id"
            ),
            {"user_id": user_id, "class_id": class_id}
        )

        # check if there are users on the waitlist has for this class, get the user with lowest position
        next_waitlist = connection.execute(
            sqlalchemy.text(
                """
                SELECT w.user_id, w.waitlist_position, u.username
                FROM waitlist w
                JOIN users u ON w.user_id = u.user_id
                WHERE w.class_id = :class_id
                ORDER BY w.waitlist_position
                LIMIT 1
                """
            ),
            {"class_id": class_id}
        ).first()

        if next_waitlist:
            next_user_id = next_waitlist.user_id
            next_user_username = next_waitlist.username

            # remove user from waitlist
            connection.execute(
                sqlalchemy.text(
                    "DELETE FROM waitlist WHERE user_id = :user_id AND class_id = :class_id"
                ),
                {"user_id": next_user_id, "class_id": class_id}
            )

            # insert booking for user
            connection.execute(
                sqlalchemy.text(
                    "INSERT INTO bookings (user_id, class_id) VALUES (:user_id, :class_id)"
                ),
                {"user_id": next_user_id, "class_id": class_id}
            )

            # shift waitlist positions for the class
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE waitlist
                    SET waitlist_position = waitlist_position - 1
                    WHERE class_id = :class_id
                    """
                ),
                {"class_id": class_id}
            )

    return CancelResponse(
        class_id=class_id,
        cancellation_status="Booking cancelled successfully",
        enrolled_from_waitlist=next_user_username if next_waitlist else None,
    )

@router.get("/{class_id}/waitlist")
def get_waitlist(class_id: int):
    """
    Get all users on the waitlist for a class
    """
    start_time = time.time()
    with db.engine.begin() as connection:
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

        # get all users on the waitlist
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT u.username, w.waitlist_position
                FROM waitlist w
                JOIN users u ON w.user_id = u.user_id
                WHERE w.class_id = :class_id
                ORDER BY w.waitlist_position
                """
            ),
            {"class_id": class_id}
        )

        waitlist = [{"username": row.username, "waitlist_position": row.waitlist_position} for row in result]

    return {"class_id": class_id, "waitlist": waitlist}

class JoinWaitlistResponse(BaseModel):
    username: str
    class_id: int
    waitlist_position: int

@router.post("/{class_id}/waitlist/join")
def join_waitlist(class_id: int, username: str):
    """
    Join the waitlist for a class
    """
    start_time = time.time()
    with db.engine.begin() as connection:
        # check if user exists
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

        # check if user is already booked for the class
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
            raise HTTPException(status_code=422, detail="User already booked this class")

        # check if user is already on the waitlist
        existing_waitlist = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 FROM waitlist 
                WHERE user_id = :user_id AND class_id = :class_id
                """
                ),
            {"user_id": user_id, "class_id": class_id}
        ).first()

        if existing_waitlist:
            raise HTTPException(status_code=400, detail="User already on the waitlist")

        # get current waitlist position
        current_position = connection.execute(
            sqlalchemy.text(
                """
                SELECT MAX(waitlist_position) FROM waitlist 
                WHERE class_id = :class_id
                """
                ),
            {"class_id": class_id}
        ).scalar()
        # insert user into waitlist
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO waitlist (user_id, class_id, waitlist_position)
                VALUES (:user_id, :class_id, :waitlist_position)
                """
                ),
            {
                "user_id": user_id,
                "class_id": class_id,
                "waitlist_position": current_position + 1 if current_position else 1
            }
        )
    return JoinWaitlistResponse(
        username=username,
        class_id=class_id,
        waitlist_position=current_position + 1 if current_position else 1
    )

@router.get("/{username}")
def get_bookings(username: str):
    """
    Get all class bookings for a user
    """
    start_time = time.time()
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
