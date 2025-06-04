from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import List
import sqlalchemy
from src.api import auth
from src import database as db
import datetime, re

import time

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
    dependencies=[Depends(auth.get_api_key)],
)


class RoomDescription(BaseModel):
    number: int
    capacity: int
    type: str

class TimeSlot(BaseModel):
    start: datetime.time
    end: datetime.time

class RoomAvailability(BaseModel):
    number: int
    day: datetime.date
    availability_slots: List[TimeSlot]

@router.post("", status_code=status.HTTP_201_CREATED)
def create_room(room: RoomDescription):
    """
    Create a new room
    """
    with db.engine.begin() as connection:
        existing = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 FROM rooms 
                WHERE room_number = :number
                """
                ),
            {"number": room.number}
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Room with this number already exists")
        
        if room.capacity <= 0:
            raise HTTPException(status_code=400, detail="Room capacity must be a positive number")

        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO rooms (room_number, capacity, type)
                VALUES (:number, :capacity, :type)
                """
                ),
            {
                "number": room.number,
                "capacity": room.capacity,
                "type": room.type,
            }
        )

    return {"message": "Room created successfully"}


@router.get("", response_model=List[RoomDescription])
def get_rooms():
    """
    Get all rooms
    """
    start_time = time.time()
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM rooms
                """
            )
        ).all()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    return [
        RoomDescription(
            number=row.room_number,
            capacity=row.capacity,
            type=row.type,
        )
        for row in result
    ]

@router.get("/{number}", response_model=RoomDescription)
def get_rooms_number(number: int):
    """
    Get room details by its number
    """
    start_time = time.time()
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                SELECT room_number, capacity, type 
                FROM rooms
                WHERE room_number =:number
                """
            ),{"number": number}
        ).first()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    if not row:
        raise HTTPException(status_code=404, detail="Room not found")

    return RoomDescription(
            number=row.room_number,
            capacity=row.capacity,
            type=row.type,
        )

@router.get("/availability/{date}", response_model=List[RoomAvailability])
def get_available_rooms(date: str):
    """
    Get all available rooms
    """
    track_start_time = time.time()
    result = []

    #exact match for date format YYYY-MM-DD
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise HTTPException(status_code=422, detail="Date must be in YYYY-MM-DD format")

    # Then try parsing the date
    try:
        parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date. Must be a real calendar date in YYYY-MM-DD format")
    start = datetime.time(8, 0)
    end = datetime.time(18, 0)

    #check if date is in the future
    if parsed_date < datetime.date.today():
        raise HTTPException(status_code=422, detail="Cannot check availability for past dates")

    
    with db.engine.begin() as connection:
        rooms = connection.execute(
            sqlalchemy.text(
                """
                SELECT room_number FROM rooms
                """
            )).fetchall()
                
        for room in rooms:
            room = room[0]
            bookings = connection.execute(
                sqlalchemy.text("""
                    SELECT start_time, end_time
                    FROM classes
                    WHERE room_number = :room AND day = :day
                    ORDER BY start_time
                """),
                {"room": room, "day": date}
            ).fetchall()

            available_slots= []
            current_time = start
            
            for booking in bookings:
                if current_time != booking.start_time:
                    available_slots.append({"start": current_time, "end": booking.start_time})
                current_time = booking.end_time

            if current_time != end:
                available_slots.append({"start": current_time, "end": end})
    
            if not bookings:
                available_slots = [{"start": "06:00", "end": "18:00"}]

            result.append(RoomAvailability(number = room, day = date, availability_slots = available_slots))
    track_end_time = time.time()
    elapsed_time = track_end_time - track_start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    return result