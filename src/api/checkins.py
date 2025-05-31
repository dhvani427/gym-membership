from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List
import sqlalchemy
from src.api import auth
from src import database as db
from datetime import date, datetime,time

router = APIRouter(
    prefix="/checkins",
    tags=["checkins"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/{user_id}/checkin", status_code=status.HTTP_204_NO_CONTENT)
def checkin_user(user_id: int):
    """
    Check in a user by inserting a row into the history table.
    """
    now = datetime.now()

    with db.engine.begin() as connection:
        # check if user exists
        user = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 
                FROM users 
                WHERE user_id = :user_id
                """),
            {"user_id": user_id}
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User does not exist. Cannot check in."
            )

        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO history (check_in_date, check_in_time, user_id)
                VALUES (:check_in_date, :check_in_time, :user_id)
                """
            ),
            {
                "user_id": user_id,
                "check_in_date": now.date(),
                "check_in_time": now.time(),
            }
        )

class CheckinHistory(BaseModel):
    check_in_date: date
    check_in_time: time  

@router.get("/users/{user_id}/checkins", response_model=List[CheckinHistory])
def get_user_checkins(user_id: int):
    """
    Retrieve a user's checkin history.
    """
    with db.engine.begin() as connection:
        # check if user exists
        user = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 
                FROM users 
                WHERE user_id = :user_id
                """),
            {"user_id": user_id}
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User does not exist. Cannot retrieve check-in history."
            )

        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT check_in_date, check_in_time 
                FROM history 
                WHERE user_id = :user_id
                """
            ),
            {"user_id": user_id}
        ).fetchall()

        return [
            CheckinHistory(
                check_in_date=row.check_in_date,
                check_in_time=str(row.check_in_time)
            )
            for row in result
        ]
