from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
import sqlalchemy
from src.api import auth
from src import database as db
from datetime import date, time


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
    start: time
    end: time

class RoomAvailability(BaseModel):
    number: int
    day: date
    availability_slots: List[TimeSlot]



@router.get("", response_model=List[RoomDescription])
def get_rooms():
    """
    Get all rooms
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM rooms
                """
            )
        ).all()

    return [
        RoomDescription(
            number=row.room_number,
            capacity=row.capacity,
            type=row.type,
        )
        for row in result
    ]

@router.get("/{number}", response_model=List[RoomDescription])
def get_rooms_number(number: int):
    """
    Get all room numbers
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM rooms
                WHERE room_number =:number
                """
            ),{"number": number}
        ).all()

    return [
        RoomDescription(
            number=row.room_number,
            capacity=row.capacity,
            type=row.type,
        )
        for row in result
    ]

@router.get("/{day}", response_model=List[RoomAvailability])
def get_available_rooms(day: date):
    """
    Get all available rooms
    """
    result = []
    start = time(8,0)
    end = time(18,0)
    
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
                {"room": room, "day": day}
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


            result.append(RoomAvailability(number = room, day = day, availability_slots = available_slots))
        
    return result