from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List
import sqlalchemy
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/membership",
    tags=["membership"],
    dependencies=[Depends(auth.get_api_key)],
)

class MembershipPlan(BaseModel):
    membership_id: int
    membership_plan: str
    cost: int
    max_classes: int

class EnrollRequest(BaseModel):
    membership_id: int

class EnrollResponse(BaseModel):
    message: str

@router.post("/membership/{username}/enroll", response_model=EnrollResponse)
def enroll_in_plan(username: str, data: EnrollRequest):
    """
    Enroll a user in a membership plan by username
    """
    with db.engine.begin() as connection:
        user = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM users WHERE username = :username
                """
                ),
            {"username": username}
        ).fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        if user.membership_id is not None:
            raise HTTPException(
                status_code=400,
                detail="User already enrolled in a plan. Please upgrade if you want a different plan."
            )

        plan = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM membership WHERE membership_id = :membership_id
                """
            ),
            {"membership_id": data.membership_id}
        ).fetchone()

        if not plan:
            raise HTTPException(status_code=404, detail="Membership plan not found.")

        connection.execute(
            sqlalchemy.text(
                """
                UPDATE users
                SET membership = :membership_id
                WHERE username = :username
                """
            ),
            {"username": username, "membership_id": data.membership_id}
        )
    return EnrollResponse(message="User successfully enrolled in membership plan.")

class MembershipResponse(BaseModel):
    membership_id: int
    membership_plan: str
    cost: int
    max_classes: int

@router.get("/membership/plans", response_model=List[MembershipResponse])
def get_membership_plans():
    """
    Get all membership plans
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM membership
                """
            )
        ).all()

    return [
        MembershipResponse(
            membership_id=row[0],
            membership_plan=row[1],
            cost=row[2],
            max_classes=row[3]
        )
        for row in result
    ]