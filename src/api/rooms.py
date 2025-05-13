from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
import sqlalchemy
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
    dependencies=[Depends(auth.get_api_key)],
)


class RoomDescription(BaseModel):
    number: int
    capacity: int
    type: str

@router.get("/rooms", response_model=List[RoomDescription])
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
            number=row[0],
            capacity=row[1],
            type=row[2],
        )
        for row in result
    ]

@router.get("/rooms/:number", response_model=List[RoomDescription])
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
            number=row[0],
            capacity=row[1],
            type=row[2],
        )
        for row in result
    ]