from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, PositiveInt
from typing import List
import sqlalchemy
from src.api import auth
from src import database as db

import time

router = APIRouter(
    prefix="/membership",
    tags=["membership"],
    dependencies=[Depends(auth.get_api_key)],
)

class MembershipPlan(BaseModel):
    membership_plan: str = Field(..., min_length=1)
    cost: PositiveInt = Field(..., gt=0)
    max_classes: int = Field(..., ge=0)

@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def enroll_in_plan(username: str, membershipPlan: MembershipPlan):
    """
    Create new membership plan
    """
    start_time = time.time()
    with db.engine.begin() as connection:
        # check for duplicate plan name
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM membership
                WHERE membership_plan = :membership_plan
                """
                ),
            {"membership_plan": membershipPlan.membership_plan}
        ).fetchone()

        # insert new plan
        if result:
            raise HTTPException(
                status_code=400,
                detail="Plan already exists."
            )
        else:
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO membership (membership_plan, cost, max_classes)
                    VALUES (:membership_plan, :cost, :max_classes)
                    """
                ),
                {
                    "membership_plan": membershipPlan.membership_plan,
                    "cost": membershipPlan.cost,
                    "max_classes": membershipPlan.max_classes
                }
            )
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")

class EnrollRequest(BaseModel):
    membership_id: int

class EnrollResponse(BaseModel):
    message: str

@router.post("/{user_id}/enroll", response_model=EnrollResponse)
def enroll_in_plan(user_id: str, data: EnrollRequest):
    """
    Enroll a user in a membership plan by username
    """
    start_time = time.time()
    with db.engine.begin() as connection:
        # fetch the user by username
        user = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM users WHERE user_id = :user_id
                """
                ),
            {"user_id": user_id}
        ).fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        if user.membership is not None:
            raise HTTPException(
                status_code=400,
                detail="User already enrolled in a plan. Please upgrade if you want a different plan."
            )

        # validate the requested membership plan
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

        # update user’s membership
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE users
                SET membership = :membership_id
                WHERE user_id = :user_id
                """
            ),
            {"user_id": user_id, "membership_id": data.membership_id}
        )

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    return EnrollResponse(message="User successfully enrolled in membership plan.")

class MembershipResponse(BaseModel):
    membership_id: int
    membership_plan: str
    cost: int
    max_classes: int

@router.get("/plans", response_model=List[MembershipResponse])
def get_membership_plans():
    """
    Get all membership plans
    """
    start_time = time.time()
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT * FROM membership
                """
            )
        ).all()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    return [
        MembershipResponse(
            membership_id=row[0],
            membership_plan=row[1],
            cost=row[2],
            max_classes=row[3]
        )
        for row in result
    ]