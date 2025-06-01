## Feedback 1: Rohan Udupa
--
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
--
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

## Feedback 3: Alex
--
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
