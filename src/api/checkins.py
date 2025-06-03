from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List
import sqlalchemy
from src.api import auth
from src import database as db
import datetime

import time

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
    start_time = time.time()
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
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")

class CheckinHistory(BaseModel):
    check_in_date: datetime.date
    check_in_time: datetime.time

@router.get("/{user_id}", response_model=List[CheckinHistory])
def get_user_checkins(user_id: int):
    """
    Retrieve a user's checkin history.
    """
    start_time = time.time()
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

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")

        return [
            CheckinHistory(
                check_in_date=row.check_in_date,
                check_in_time=str(row.check_in_time)
            )
            for row in result
        ]
