from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field

import sqlalchemy
from src.api import auth
from src import database as db
from datetime import date
from fastapi.responses import JSONResponse

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

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: User):
    """
    Register a new user. Check for duplicate username or email first. Return user_id on success.
    """
    username = f"{user.username}"

    with db.engine.begin() as connection:
        # Check for existing username
        existing = connection.execute(
            sqlalchemy.text("SELECT 1 FROM users WHERE username = :username"),
            {"username": user.username}
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

        # Check for existing email
        existing_email = connection.execute(
        sqlalchemy.text("SELECT 1 FROM users WHERE email = :email"),
        {"email": user.email}
        ).first()

        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Register a new user
    with db.engine.begin() as connection:
        id = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO users (username, password, date_of_birth, first_name, last_name, email)
                VALUES (:username, :password, :date_of_birth, :first_name, :last_name, :email)
                RETURNING user_id
                """
            ),{
                "username": user.username,
                "password": user.password,
                "date_of_birth": user.date_of_birth,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
        )
        user_id = id.scalar()

    return JSONResponse(status_code=201, content={"message": "User registered successfully", "user_id": user_id})


class UserResponse(BaseModel):
    username: str
    date_of_birth: date
    first_name: str
    last_name: str
    email: str

@router.get("/{user_id}", response_model=UserResponse)
def get_user_info(user_id:str):
    """
    Get user details
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM users 
                WHERE user_id = :user_id
                """
            ),{
                "user_id": f"{user_id}",

            }
        )
        user = result.fetchone()
        print(user)

    # Check if user exists
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        username=user[1],
        date_of_birth=user[5],
        first_name=user[2],
        last_name=user[3],
        email=user[4]
    )
