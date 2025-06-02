from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field

import sqlalchemy
from src.api import auth
from src import database as db
from datetime import date

import time

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    username: str
    password: str
    date_of_birth: date
    first_name: str
    last_name: str
    email: str


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def register_user(user: User):
    """
    Registering a user to the gym
    """
    start_time = time.time()
    username = f"{user.username}"

    # check if the user already exists
    with db.engine.begin() as connection:
        existing = connection.execute(
            sqlalchemy.text(
                "SELECT 1 FROM users WHERE username = :username"
            ),
            {"username": username}
        ).first()

        if existing:
            raise HTTPException(status_code=409, detail="User already exists")

        # insert the new user if not already present
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO users (username, password, date_of_birth, first_name, last_name, email)
                VALUES (:username, :password, :date_of_birth, :first_name, :last_name, :email)
                """
            ),{
                "username": f"{user.username}",
                "password": f"{user.password}",
                "date_of_birth": f"{user.date_of_birth}",
                "first_name": f"{user.first_name}",
                "last_name": f"{user.last_name}",
                "email": f"{user.email}",

            }
        )
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

class UserResponse(BaseModel):
    username: str
    date_of_birth: date
    first_name: str
    last_name: str
    email: str


@router.get("/{username}", response_model=UserResponse)
def get_user_info(username:str):
    """
    Get user details
    """
    start_time = time.time()
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM users 
                WHERE username = :username
                """
            ),{
                "username": f"{username}",

            }
        )
        user = result.fetchone()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    return UserResponse(
        username=user.username,
        date_of_birth=user.date_of_birth,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    )
