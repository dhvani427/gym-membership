from fastapi import APIRouter, Depends, HTTPException, status
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
    name: str
    cost: int
    max_classes: int

@router.post("/membership", status_code=status.HTTP_204_NO_CONTENT)
def create_plan(membershipPlan: MembershipPlan):
    """
    Create new membership plan
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM membership
                WHERE name = :membership_plan
                """
                ),
            {"membership_plan": membershipPlan.name}
        ).fetchone()

        if result:
            raise HTTPException(
                status_code=400,
                detail="Plan already exists."
            )
        else:
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO membership (name, cost, max_classes)
                    VALUES (:membership_plan, :cost, :max_classes)
                    """
                ),
                {
                    "membership_plan": membershipPlan.name,
                    "cost": membershipPlan.cost,
                    "max_classes": membershipPlan.max_classes
                }
            )

class EnrollRequest(BaseModel):
    name: str

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

        if user[7] is not None:
            raise HTTPException(
                status_code=400,
                detail="User already enrolled in a plan. Please upgrade if you want a different plan."
            )

        plan = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM membership WHERE name = :name
                """
            ),
            {"name": data.name}
        ).fetchone()

        if not plan:
            raise HTTPException(status_code=404, detail="Membership plan not found.")

        connection.execute(
            sqlalchemy.text(
                """
                UPDATE users
                SET membership_plan = :membership_plan
                WHERE username = :username
                """
            ),
            {"username": username, "membership_plan": plan[0]}
        )
    return EnrollResponse(message="User successfully enrolled in membership plan.")

class MembershipResponse(BaseModel):
    membership_id: int
    name: str
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
            name=row[1],
            cost=row[2],
            max_classes=row[3]
        )
        for row in result
    ]