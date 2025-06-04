from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.responses import JSONResponse


import sqlalchemy
from src.api import auth
from src import database as db

import datetime
import time

router = APIRouter(
    prefix="/classes",
    tags=["classes"],
    dependencies=[Depends(auth.get_api_key)],
)

class Class(BaseModel):
    class_name: str
    class_type: str
    description: str
    day: datetime.date
    capacity: int
    start_time: datetime.time = Field(..., example="18:00")
    end_time: datetime.time = Field(..., example="19:00")
    instructor: str
    room_number: int


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_class(gym_class: Class):
    """
    Posting a class
    """
    endpoint_start_time = time.time()

    # Check if the room exists
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
        # Check if class capacity is positive and does not exceed room capacity
        if gym_class.capacity <= 0:
            raise HTTPException(status_code=400, detail="Class capacity must be a positive number")

        #if class capacity is more than room capacity
        if gym_class.capacity > room_capacity:
            raise HTTPException(
                status_code=400,
                detail=f"Class capacity {gym_class.capacity} exceeds room capacity {room_capacity}"
            )
        
        # Check that start time is before end time
        if gym_class.start_time>gym_class.end_time:
            raise HTTPException(
                status_code=400,
                detail=f"Class start time must be before the end time"
            )
        
        #Check if time is within gym hours (e.g., 6am - 10pm)
        opening = datetime.time(6, 0)
        closing = datetime.time(18, 0)
        if not (opening <= gym_class.start_time <= closing and opening <= gym_class.end_time <= closing):
            raise HTTPException(
                status_code=400,
                detail="Class must be scheduled between 6:00 AM and 6:00 PM"
            )
        
        #check if the duration of the class exceeds 2 hours
        start_dt = datetime.datetime.combine(gym_class.day, gym_class.start_time)
        end_dt = datetime.datetime.combine(gym_class.day, gym_class.end_time)
        duration = (end_dt - start_dt).total_seconds() / 3600
        if duration > 2:
            raise HTTPException(
                status_code=400,
                detail="Class duration cannot exceed 2 hours"
            )
        
        # Check if trying to schedule class in the past
        now = datetime.datetime.now()
        class_datetime = datetime.datetime.combine(gym_class.day, gym_class.start_time)
        if class_datetime < now:
            raise HTTPException(
                status_code=400,
                detail="Cannot schedule a class in the past"
            )
        
        # Check for duplicate class
        duplicate = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 FROM classes
                WHERE class_name = :class_name AND day = :day
                AND start_time = :start_time AND instructor = :instructor
                AND room_number = :room_number
                """
            ),
            {
                "class_name": gym_class.class_name,
                "day": gym_class.day,
                "start_time": gym_class.start_time,
                "instructor": gym_class.instructor,
                "room_number": gym_class.room_number
            }
        ).first()

        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Duplicate class: this class has already been added"
            )
        
        # Check for room conflict with time overlap
        conflict = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 FROM classes
                WHERE room_number = :room_number
                AND day = :day
                AND (
                    (start_time < :start_time AND end_time > :start_time)
                    OR
                    (start_time >= :start_time AND start_time < :end_time)
                    OR
                    (start_time <= :start_time AND end_time >= :end_time)
                )
                """
            ),
            {
                "room_number": gym_class.room_number,
                "day": gym_class.day,
                "start_time": gym_class.start_time,
                "end_time": gym_class.end_time
            }
        ).first()

        if conflict:
            raise HTTPException(
                status_code=409,
                detail="Room already booked during the selected time slot"
            )

        
        # Check for instructor conflict
        instructor_conflict = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 FROM classes
                WHERE instructor = :instructor
                AND day = :day
                AND (
                    (start_time < :start_time AND end_time > :start_time)
                    OR
                    (start_time >= :start_time AND start_time < :end_time)
                    OR
                    (start_time <= :start_time AND end_time >= :end_time)
                )
                """
            ),
            {
                "instructor": gym_class.instructor,
                "day": gym_class.day,
                "start_time": gym_class.start_time,
                "end_time": gym_class.end_time,
            }
        ).first()

        if instructor_conflict:
            raise HTTPException(
                status_code=409,
                detail="Instructor is already teaching another class at this time"
            )

        # Proceed to insert the class
        class_id = connection.execute(
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
                RETURNING class_id
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
        # Get the class_id of the newly created class
        class_id = class_id.scalar()

        end_time = time.time()
        elapsed_time = end_time - endpoint_start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        
        return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Class created successfully", "class_id": class_id}
    )

@router.get("/search", response_model=List[Class], tags=["classes"])
def search_classes(
    class_name: str = "",
    class_type: str = "",
    instructor: str = "",
    day: Optional[datetime.date] = None,
    start_time: Optional[datetime.time] = None,
    end_time: Optional[datetime.time] = None,
):
    """
    Search for classes using optional filters.
    """
    endpoint_start_time = time.time()

    # Check for invalid time range
    if start_time and end_time and start_time > end_time:
        raise HTTPException(status_code=400, detail="Start time must be before end time")
    
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
    
    if not results:
        raise HTTPException(status_code=404, detail="No classes found")

    end_time = time.time()
    elapsed_time = end_time - endpoint_start_time
    print(f"Elapsed time: {elapsed_time} seconds")

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
