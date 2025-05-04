from fastapi import APIRouter, Depends, status
import sqlalchemy
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.post("/users", status_code=status.HTTP_204_NO_CONTENT)
def users():
    """
    Getting all the gym users
    """

    '''connection.execute(sqlalchemy.text("TRUNCATE global_ledger"))
    connection.execute(sqlalchemy.text("TRUNCATE potion_ledger"))


    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                # changed
                """
                INSERT INTO global_ledger (transaction_id, gold, red_ml, green_ml, blue_ml, dark_ml)
                VALUES ('reset_init', 100, 0, 0, 0, 0)
                """
            )
        )
    # TODO: Implement database write logic here
    pass'''