## Feedback 1: Rohan Udupa

### Code Review

**1. Redundant route naming (e.g., /users/users/register)**
Updated route paths within users.py, rooms.py, and membership.py to remove the redundant /users, /rooms, etc

**2. No user feedback when user already exists**
Added proper response message and status code

**3. NIT: In your server.py you dont have tags-metadata which means your /docs endpoint wont be updated.**
Added:
tags_metadata = [
    {"name": "users", "description": "Manage gym users"},
    {"name": "membership", "description": "Membership plans and status"},
    {"name": "classes", "description": "Fitness class schedules"},
    {"name": "bookings", "description": "Class bookings"},
    {"name": "checkins", "description": "Gym check-in logs"},
    {"name": "rooms", "description": "Room and facility management"},
]

**4. Using indices to pull out data which could break functionality if you make a schema update**
Fixed to using column names to pull out data instead of relying on indices

**5. Parameter name mismatch in /date/{date}**
Changed the whole function, to a single one that can take in filter options, so don't have that problem anymore

**6. get_by_id returns list instead of object**
Fixed to not returning an embedded list anymore

**7. get_by_id lacks None check**
Changed the whole function, to a single one that can take in filter options, so don't have that problem anymore

**8.  CheckinHistory uses str instead of date/time types**
Updated check_in_date to use datetime.date and check_in_time to use datetime.time

**10.  Missing / in {username}/bookings route**
Didn't seem to be missing

**11. No check for full classes in booking**
Added a capacity check and returning proper message

## Feedback 2: Felix

### Code Review

**1. Combine Class Filters into a Single Endpoint**
Combine into one endpoint using query parameters

**2. Hardcoded Column Indices in Query Results**
(Repeated)

**3. Inconsistent Return Type for get_by_id**
(Repeated)

**4. No None Check in get_by_id**
(Repeated)

**6. Duplicate Query Patterns**
Every query is pulling different columns and different data

**8. Unnecessary Print Statements**
For debugging purposed, removed now

**9. No Validation for Time Ranges**
Added check for whether end time is after start time, and returning appropriate message

**10. No Unique Constraint Handling**
Added a check for only unique classes get added 

**12. Ambiguous Parameter Naming in get_by_date**
Fixed so that the naming is the same

**13. No Error Handling for Empty Query Results**
Adding appropriate messages

**14. Lack of Docstrings for Most Endpoints**
All endpoints had docstrings

## Feedback 3: Alex Truong

### Code Review

**1. TRUNCATE statements in users.py**
Removed the truncate lines entirely

**2. Two transactions in /users/register**
Combined all DB operations under a single with db.engine.begin() block

**3. No client feedback for existing users**
Added message -> "User already exists. No changes made."

**4. GET /rooms and GET /rooms/{number} readability**
Using column names instead of indices now to return data

**5. membership.py return statement readability**
Using column names instead of indices now to return data

**6. bookings.py should use .first() and null check**
Added a check if no result is found and returning no booking for user message

**7. Input validation for the MembershipPlan class**
Added the following validations:
    name: str = Field(..., min_length=1)
    cost: int = Field(..., gt=0)
    max_classes: int = Field(..., ge=0)

### API/Schema
**1. The users route has two endpoints with POST /users/register and GET /users/{username}. I believe it's ideal to reduce the complexity and length of endpoints as much as possible without sacrificing readability and functionality so I would just having /users/...**
We fixed it: The users route is now just /users/...

**2.Membership also has this issue where its /membership/membership/.... I would suggest simplifying it.**
Changed to /membership/... to simplify.

**3.The bookings route has a couple issues where you can just make a POST /bookings/class_id instead of POST /bookings/{class_id}/book. Additionally, the GET/bookings/{username}/bookings can be condensed into something like GET /bookings/{username}.**
We decided to keep the POST /bookings/{class_id}/book endpoint because we added new endpoints like GET /bookings/{class_id}/waitlist. We also changed the GET /bookings/{username}/bookings endpoint to GET /bookings/{username} for simplicity, as it doesn't conflict with the other /bookings endpoints.

**4.For POST /bookings/{class_id}/book, I would suggest having the endpoint use a JSON body to input the class_id and username instead of queries. I believe for best REST API practices you want to reserve queries for GET requests(filtering, sorting, etc) and JSON bodies for the others. You can do this by just making another Pydantic class and having the function take in that class as input.**
The endpoint now accepts class_id and username in a JSON body using a Pydantic model instead of passing them in the path or query. This follows REST best practices by keeping the URL simple and using the request body for data input.

**5.The checkins route also has a similar issue where I believe it could be shortened into POST /checkins/{user_id} and GET /checkins/{user_id}.**
We kept POST /checkins/{user_id}/checkin for when a user checks in, but changed the GET to /checkins/{user_id} because it’s simpler and easier for users to understand.

**6.Rooms route also has similar issue. Instead, have GET /rooms and GET /rooms/:number.**
fixed

**7.membership.cost should always be positive.**
cost: PositiveInt = Field(..., gt=0, description="Cost of the membership plan in dollars")

**8.There should be a foreign key relation between bookings.class_id and classes.class_id.**
We already have th relationship: 
	sa.Column("class_id", sa.Integer, sa.ForeignKey("classes.class_id"), nullable=False),

**9.Consider making endpoints to unenroll from a booking and remove a class**
We added those in the v4:
@router.delete("/{class_id}/cancel", response_model=CancelResponse)
def cancel_booking(class_id: int, username: str):

**10.I think a majority GET endpoints for the /classes/... route can be condensed down into one singular function where you add optional queries. that way you use less endpoints and have a more concise endpoint that does everything.**
We moved everything in one search endpoint in v4:
@router.get("/search", response_model=List[Class], tags=["classes"])
def search_classes(
   class_name: str = "",
   class_type: str = "",
   instructor: str = "",
   day: Optional[date] = None,
   start_time: Optional[time] = None,
   end_time: Optional[time] = None,
):

**11.Add start/end dates for memberships?**
We didn’t add start/end dates because the membership becomes active from the user’s first checkin_date which we already have in the db. All memberships last one month, we can calculate the period based on that first check-in if needed, without needing extra fields.

**12.Consider adding alembic CheckConstraints for things like cost or class capacity.**
We added constraints for fields like cost and class capacity in v4.

## Feedback 4: Shane

### Code Review

**1. Adding extra comments to users.py**
Added comments for context

**2. Replacing print with HTTP**
Replaced with raise HTTPException(status_code=409, detail="User already exists")

**3. Adding extra comments to membership.py**
Added comments for context

**4. Checking if user exists for checkins.py.checkin_user**
raise HTTPException(status_code=404, detail="User does not exist. Cannot check in.") if user doesn't exist

**5. Checking if user exists for checkins.py.get_user_checkins**
raise HTTPException(status_code=404, detail="User does not exist. Cannot retrieve check-in history.") if user doesn't exist

**6. Change the response model for "/rooms/:number"**
Changed to response_model=RoomDescription instead of a List since it only returns one

## Feedback 5: Khoa

### Code Review

**1. Wrong comment for /users/register**
Changed to "Registering a user to the gym"



