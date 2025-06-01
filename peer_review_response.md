## Feedback 1: Rohan Udupa
--
# Code Review

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
