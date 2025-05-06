from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth
from src import database as db
from datetime import date

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


@router.post("/users/register", status_code=status.HTTP_204_NO_CONTENT)
def register_user(user: User):
    """
    Getting all the gym users
    """

    '''connection.execute(sqlalchemy.text("TRUNCATE global_ledger"))
    connection.execute(sqlalchemy.text("TRUNCATE potion_ledger"))'''


    username = f"{user.username}"

    with db.engine.begin() as connection:
        existing = connection.execute(
            sqlalchemy.text(
                "SELECT 1 FROM users WHERE username = :username"
            ),
            {"username": username}
        ).first()

        if existing:
            print("Transaction already processed.")
            return


    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                # changed
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


class UserResponse(BaseModel):
    username: str
    date_of_birth: date
    first_name: str
    last_name: str
    email: str


@router.get("/users/{username}", response_model=UserResponse)
def get_user_info(username:str):
    """
    Get user details
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                # changed
                """
                SELECT * FROM users 
                WHERE username = :username
                """
            ),{
                "username": f"{username}",

            }
        )
    return UserResponse(username=result.username, date_of_birth=result.date_of_birth, first_name=result.first_name, last_name=result.last_name, email=result.email)
