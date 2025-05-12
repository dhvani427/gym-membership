from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field

import sqlalchemy
from src.api import auth
from src import database as db
from datetime import date

router = APIRouter(
    prefix="/classes",
    tags=["classes"],
    dependencies=[Depends(auth.get_api_key)],
)

class Class(BaseModel):
    class_name: str
    class_type: str
    description: str
    day: str
    capacity: int
    start_time: str
    end_time: str
    instructor: str
    room_number: int


@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def post_class(gym_class: Class):
    """
    Posting a class
    """

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT capacity FROM rooms WHERE room_number = :room_number"
            ),
            {"room_number": gym_class.room_number}
        ).fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="Room not found")

        room_capacity = result.capacity

        if gym_class.capacity > room_capacity:
            raise HTTPException(
                status_code=400,
                detail=f"Class capacity {gym_class.capacity} exceeds room capacity {room_capacity}"
            )

        # Proceed to insert the class
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO classes (
                    class_name, class_type, description, day, capacity,
                    start_time, end_time, instructor, room_number
                )
                VALUES (
                    :class_name, :class_type, :description, :day, :capacity,
                    :start_time, :end_time, :instructor, :room_number
                )
                """
            ),
            {
                "class_name": gym_class.class_name,
                "class_type": gym_class.class_type,
                "description": gym_class.description,
                "day": gym_class.day,
                "capacity": gym_class.capacity,
                "start_time": gym_class.start_time,
                "end_time": gym_class.end_time,
                "instructor": gym_class.instructor,
                "room_number": gym_class.room_number,
            }
        )
