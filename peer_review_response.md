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

##API/Schema
**1.I was wondering why the membership cart endpoint is a PUT. I believe a put is usually used to mean that a user is replacing or updating an existing resource. I don't think this is happening in this case, perhaps it should just be a POST.**
Fixed this, I believe this is what this comment is referring too but there is also no other instances of Put, so either way it is good.
	
**2.A lot of current endpoints seem to return a success boolean response which can be a bit vague and hard for the user what to fix if it is an issue on their end or instead an internal error. Perhaps use error codes and specified message responses when required like such:
{
  "message": "User enrolled in class successfully"
}**
We have gone through and implemented a lot better responses, there is still room for improvement for specific endcases, but we have made a lot of improvements that make our code much more readable and understandable if there is an error.

**3.There seems to be a few naming inconsistencies in some endpoints which can make it a bit confusing for the user if they are referring to the same thing. Ex. class is used in some places where class_name are used in others also cost and price. Perhaps unify these.**
We fixed redundancies and cut down on our endpoints for clarity, most notably in users and membership. 

**4.In all endpoints with inputs it is most likely best to take in an id. For a few endpoints it takes a users username which can perhaps change. Instead it may make more sense to take in a user_id.**
We don’t have a possibility for the username to change right now so this isn’t really a worry at the moment. Also some of the id’s are generated with the creation of that row in the table so it is not necessarily something that the user might just automatically know off the top of their head. In this case we found it easier to use usernames versus remembering a random number. 

**5.Your current flow references a query param that allows you to filter classes of specific types but this doesn't seem to be defined in the api spec. This endpoint GET /classes?type=yoga. Perhaps update the intended functionality or enable a filter by adding another parameter to the class type.**
We changed the git classes endpoint, and now it is GET /classes/search so you can search by different optional parameters such as date, name, instructor, ect.

**6.Perhaps specific endpoints should be limited to specific users. In the flows there seems to be two main user types, an instructor and a member; they can perhaps have respective endpoints such as either having the ability to create a class or enroll in a class based on their account type.**
Included more restrictions in code review.

**7.It seems logical for an instructor user type to be able to view all members enrolled in their class and some basic information about them. Maybe this can be a new endpoint. This can also be tied into if the user has checked into the class yet.**
This is a good suggestion for the future just not something we had time to implement given the current state of the product and what we deem as the most important endpoints.

**8.The cart membership logic seems a bit too complex. Instead of allowing a user to grant themselves a membership id as parameter to the cart function, maybe just enter a new row into the membership table and inform a user of the membership id they were assigned.**
We liked that a user could choose the type of membership by selecting the membership id they want.

**9.Spec vs API vs Code Inconsistencies. Their seems to be a few minor consistencies between the docs and the code itself and I am not exactly sure what is the source of truth. Perhaps formatting the API spec to match what is implemented can be useful to others**
This api spec was from v2 so it has some differences as we have improved the design.

**10.Building off a previous suggestion perhaps store useful class metadata in a specific class made that allows users to filter classes apart from just date to pinpoint classes that best match their taste and interest. Perhaps filtering by intensity or instructor can be useful.**
Added alot more filters and preferences such as, date, time, instructor, day, ect

**11.It may be useful to allow users to waitlist for a specific class that is currently full. Since users have the ability to drop a class, it makes sense to allow users to waitlist a class instead if waiting for a spot to open up. This could be a queue of user_ids for each class that gets enrolled to the class as members drop.**
Great Idea, we have /bookings/{class_id}/waitlist/join and /bookings/{class_id}/waitlist inorder to join the waitlist and see a waitlist for a certain class. Furthermore if you try to enroll in a class and it is full there is a notification saying it is full and to please join the waitlist. 

**12.If users fail to check in to a class that they booked, maybe there can be a new notification service that tells a user their upcoming classes and times. If a user doesn't respond to notification they can maybe get automatically dropped from a class.**
Good Idea but I feel like this would make more sense to implement if we had a web or app platform. This is something we don’t see as essential to implement right now but definitely a good idea for a later date when we can have something similar to the potion shop website that could actually post individual user notifications. 


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

###API / Schema

**1.One of the first things I noticed is that the classes table doesn't have any sort of unique constraint to prevent duplicates. So technically, you could add the same class (same name, day, and start time) multiple times. Adding a unique constraint here would help avoid that kind of mess-up.**
This was also fixed in code review

**2.Right now, the API has separate endpoints for each filter (like filtering by name, type, date, etc.), which feels kind of clunky. It’d be way more flexible if the main classes endpoint just accepted query parameters so users could mix and match filters in one request.**
We just have one endpoint /classes/search which has different parameters, i think that is what this comment is referring to. 

**3.There’s no ID on the classes endpoint, which could become a big problem if the number of classes gets large. It’d be smart to add skip and limit parameters to avoid performance issues and help manage bigger data sets.**
A class id gets created when a class is created so this way we don’t have random numbers and it is more systematic. 

**4.The Class model doesn’t include a unique ID, which makes it harder to update or delete specific classes. Adding an ID to the schema and API responses would make things way more manageable.**
We chose to just use the class name because the id is something generated in the table when created so something that is less accessible versus the user knowing what they imputed as the name.

**5.There’s no check to make sure that end_time is actually after start_time when creating a class. That could lead to weird or broken schedules, so adding that validation would definitely help.**
Made this fix in code review
if gym_class.start_time>gym_class.end_time:
   raise HTTPException(
       status_code=400,
       detail=f"Class start time is after the end time"
   )

**6.You can assign an instructor to a class even if they don’t exist in the system. It’d be better to add a foreign key constraint or at least some validation to make sure the instructor is real.**
This is not really relevant because not ever instructor has to be a user and there can be an instructor being in a class without being a user.

**7.There’s no DELETE endpoint for classes, which makes it harder to clean up or update the schedule. Adding that would give users more control.** 
We were thinking that the classes are usually regular and pretty set in stone, but this is definitely something we could add in later, we made sure to have a delete bookings for individual user clean up.

**8.The schema doesn’t use cascading deletes. So if an instructor or room gets deleted, the related classes just hang there orphaned. Adding cascading deletes would keep things consistent.**
Right now this insn’t possible but as our system grows it is something that could be useful to note in the future.

**9.Some of the API responses (like for enroll or check-in) only return a boolean or minimal info. It’d be more helpful if they included more details, like class info or check-in time, so the user gets useful feedback.**
We have gone through and added much better documentation when something goes wrong so the user has better feedback

**10.The get_by_id endpoint returns a list with one item instead of a single object, which is kind of weird and not really REST-friendly. It should just return the object or a 404 if it doesn’t exist.**
We have it like this because a user can have multiple check ins in the history, so that we can return the full history we chose to return a list.

**11.There’s no error message or 404 if get_by_name or get_by_type finds nothing, which could be confusing. Returning a helpful message would improve the user experience.**
We created a new user response class that returns the user information. 

**12.Right now, any user can be an instructor, which might be too open. It might be better to separate instructors and users into different tables. That way, it’s easier to manage permissions and build instructor-specific features later on.**

Yes, definitely something we can add in later on, for right now we liked that because all instructors are members and can take classes in our gym they are all technically users. 


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

##API/schema
**1.The first thing that I noticed that could be improved is adding the "unique" constraint to the users.email column. Since in real-life situations, typically each account is linked to a single email.**
We added the email check in the POST users/register endpoint to prevent multiple accounts using the same email.

**2.Another improvement that could be made is for bookings. I know that you already perform a check in the code to ensure no duplicate bookings can exist for a given user_id, but you could also fix this by adding the "unique" constraint to the bookings table, particularly in relation to (user_id, class_id).**
We added user not found, booking already exists, and class not found constraints. We check if combination user and class id already exist, and checking if class is full and if it is user is prompted choose another class or join the waitlist.

**3.If you wanted to improve the schema further, I would suggest implementing some validation checks for class duration, since currently start_time and end_time have no relation. To do this, I would simply ensure that end_time > start_time. (Never ends before it starts, always ensures a valid class time)**
We added this, this was repeated from another student’s comment above
if gym_class.start_time>gym_class.end_time:
   raise HTTPException(
       status_code=400,
       detail=f"Class start time is after the end time"
   )

**4.In the alembic setup, I would possibly initialize some default classes in the classes table. (Currently they are all initialized as empty, so there is no way to run through some of the example flows as they are currently provided. I.e. For Flow 1, there are no valid classes fitting the type yoga, since there are no classes in the table)**
We manually added classes to the database to create our data in version 4.

**5.In the creation of the history table, you define the check_in_date and check_in_time as Strings, when they should be stored as Date or Time types.**
We addressed these issues in a new revision - column types were updated and existing values set to current date and time.

**6.The last improvement I would suggest for the schema formatting is to set up foreign key cascading on deletion, since currently none of your foreign keys are set to this. So, in the case of a reset, or when rows are deleted, it may lead to Null values appearing. (Or some other hard-to-track errors)**
This is a good idea for the future but we don’t have a delete user endpoint so this doesn’t apply to us right now. Therefore the foreign key constraint can’t be violated currently. The only delete or reset endpoint is with bookings and this doens’t violate any foreign key constraints. 

**7.As for the API Specs, one improvement I would make to checkout would be to provide some important context to the user upon checkout, such as their selected membership. Currently, it only returns a boolean response if it was successful.**
We have a separate endpoint where you can get all of this information for a specific user

**8.Once again, I would also change your return value for the check-in endpoint, since it currently only returns a boolean. You could set it to return to the user information, such as their check-in time, and the class they checked into.**
We return 404 no content meaning its successful and if it isn’t successful it returns a validation error.

**9.Once more, I would also change the return value for the enroll endpoint. Instead of only a boolean, you can provide info related to the class, such as the description, day, capacity, or any other related information from the classes table. (Provide the user with some context, rather than a Success/Failure)**
We return class id and booking successful or fail.

**10.Also in the API Specs, you define classes differently than in your Alembic schema definition, including the parameters duration and difficulty. I would suggest updating either the alembic or APISpec to avoid future confusion.**
This was old for version 2, so it doesn't match the changes we have made.

**11.I would implement some sort of DELETE bookings, since currently this is used in one of your example flows, but does not show up anywhere in the API documentation.**
Implemented this
We added it in the v4:
@router.delete("/{class_id}/cancel", response_model=CancelResponse)
def cancel_booking(class_id: int, username: str):

**12.This is a more general suggestion, but I would possibly separate the users and instructors into separate tables, rather than allowing all users to create classes. (Since, to my knowledge, random gym users are not able to simply walk in and teach their own course, they would need certification and approval from the gym itself) This could also allow for further development with only the instructor available endpoints. (Such as messaging their class with tips and tricks, or numerous other scenarios.**
I understand this point, we can add in more restrictions in the future but we liked having the instructors as users because they have a membership as well that comes with their employment, but I see how this suggestion could be another good strategy with different benefits 


## Feedback 5: Khoa Nguyen

### Code Review

**1. Wrong comment for /users/register**
Changed to "Registering a user to the gym"

**2. Hash passwords**
Not in the scope of the project so not implementing

**3. Consider using helper functions**
Not implementing so that we can be more flexible with the queries in case we need to change it

**4. Consider using request models**
We have multiple request models implemented

## API/Schema
**1.consider using the the actual time datatypes for instead of string check_in_date and check_in_time.**
We addressed these issues in a new revision - column types were updated and existing values set to current date and time.

**2.Bookings is not unique. Add UNIQUE(user_id, class_id) to prevent a user from being have duplicate/multiple same bookings.**
We are checking if the booking already exists before creating a new one.

**3.I noticed that you had room and class capacity. I could see an argument where the room is big enough for x amount of people but you only want y amount of people to be in that class. However if this wasn't a design intention, then consider removing classes.capacity and relying solely on the room’s capacity to avoid redundancy/inconsistencies.**
Yes, that was our intention as some instructors may prefer smaller class sizes even if the room allows more, so we kept classes.capacity separate for flexibility.

**4.For membership_id in apispec.md: The example responses use "integer" as a placeholder type, which is not incorrect, but consider showing actual sample values (e.g., 1, 29) to avoid confusion and mimic a real response.**
We used integer as a placeholder because that’s how we show types consistently for all other responses in the file. This keeps the format uniform throughout the spec.

**5.Consider making user email unique to avoid accounts being created under the same email.**
We added the email check in the POST users/register endpoint to prevent multiple accounts using the same email.

**6.Bookings could possibly include a timestamp to track when the booking was created by a certain user.**
In the current state of the project, we don’t need to track booking timestamps, but we will consider adding this feature in the future.

**7.some endpoints like @router.post("/membership/{username}/enroll") uses username while @router.post("/checkins/{user_id}/checkin") uses an id for actions on a specific user. It is probably a good idea to pick, one and stick with it for consistency**
We changed the endpoints to use user_id only for consistency.

**8.Consider adding a status column for booking that contains info such as (pending, booked, ...)**
When a booking is made, if the class has space, it’s immediately valid and added to the bookings table. If the class is full, the booking is considered pending and the user is added to the waitlist table. We use separate tables to track this instead of a status column, but adding a status field could be an alternative way to manage booking states.

**9.Consider adding an endpoint to undo/remove a booking that user no longer wants**
We added it in the v4:
@router.delete("/{class_id}/cancel", response_model=CancelResponse)
def cancel_booking(class_id: int, username: str):

**10.The room endpoint doesn't seem like it is checking for classes time overlap. Might want to be wary of that**
If you mean the get available rooms for the day endpoint, we are checking if classes overlap:
for room in rooms:
           room = room[0]
           bookings = connection.execute(
               sqlalchemy.text("""
                   SELECT start_time, end_time
                   FROM classes
                   WHERE room_number = :room AND day = :day
                   ORDER BY start_time
               """),
               {"room": room, "day": day}
           ).fetchall()


           available_slots= []
           current_time = start
          
           for booking in bookings:
               if current_time != booking.start_time:
                   available_slots.append({"start": current_time, "end": booking.start_time})
               current_time = booking.end_time


           if current_time != end:
               available_slots.append({"start": current_time, "end": end})





**11.Instructors could be it's own tables and be referenced using id rather than plain text just like users.**
Instructors can also be users with membership plans, so an instructor is essentially just a user in our system. That's why we keep instructors' data in the same table as users, instructors are also users.

**12.Consider adding a class_id to history table to track class check in or general check in also**
The history table tracks all user check-ins, including general gym visits without classes. We can use joins between history, bookings, and classes to identify class attendance without adding class_id to history. This keeps check-ins flexible for both classes and non-class visits.









