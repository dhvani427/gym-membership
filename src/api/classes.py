from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional


import sqlalchemy
from src.api import auth
from src import database as db
from datetime import date, time

router = APIRouter(
    prefix="/classes",
    tags=["classes"],
    dependencies=[Depends(auth.get_api_key)],
)

class Class(BaseModel):
    class_name: str
    class_type: str
    description: str
    day: date
    capacity: int
    start_time: time
    end_time: time
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

@router.get("/search", response_model=List[Class], tags=["classes"])
def search_classes(
    class_name: str = "",
    class_type: str = "",
    instructor: str = "",
    day: Optional[date] = None,
    start_time: Optional[time] = None,
    end_time: Optional[time] = None,
):
    """
    Search for classes using optional filters.
    """
    parameters = {}
    query = """
        SELECT * FROM classes WHERE 1=1
    """

    if class_name:
        query += " AND class_name ILIKE :class_name"
        parameters["class_name"] = f"%{class_name}%"

    if class_type:
        query += " AND class_type ILIKE :class_type"
        parameters["class_type"] = f"%{class_type}%"

    if instructor:
        query += " AND instructor ILIKE :instructor"
        parameters["instructor"] = f"%{instructor}%"

    if day:
        query += " AND day = :day"
        parameters["day"] = day

    if start_time:
        query += " AND start_time >= :start_time"
        parameters["start_time"] = start_time

    if end_time:
        query += " AND end_time <= :end_time"
        parameters["end_time"] = end_time

    with db.engine.begin() as connection:
        results = connection.execute(sqlalchemy.text(query), parameters).fetchall()

    return [
        Class(
            class_name=row.class_name,
            class_type=row.class_type,
            description=row.description,
            day=row.day,
            capacity=row.capacity,
            start_time=row.start_time,
            end_time=row.end_time,
            instructor=row.instructor,
            room_number=row.room_number,
        )
        for row in results
    ]
