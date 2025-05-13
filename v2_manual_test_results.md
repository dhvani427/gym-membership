# Flow 2: User Books Yoga Class

Maria filters her search to see yoga classes using the GET /classes/:type endpoint, specifically searching for the yoga class type. To check if there are any 7am classes before her corporate job starts, she uses the GET /classes/:start_time endpoint, where she finds a class named "yoga flow" at 7:00 AM. Maria books it by using the POST /classes/:id/book endpoint, with the class ID being 3. After successfully booking the class, she can view all her upcoming bookings using the GET /users/:id/bookings endpoint, confirming her spot in the 7am yoga flow session with instructor Josephine in room 9 on May 13th, 2025.

GET /classes/:type

1. curl -X 'GET' \
  'http://127.0.0.1:3000/classes/type/yoga' \
  -H 'accept: application/json' \
  -H 'access_token: brat'

2. [
  {
    "class_name": "hot yoga",
    "class_type": "yoga",
    "description": "yoga class but hot",
    "day": "2025-05-13",
    "capacity": 50,
    "start_time": "11:00:00",
    "end_time": "12:00:00",
    "instructor": "sarah",
    "room_number": 10
  },
  {
    "class_name": "yoga flow",
    "class_type": "yoga",
    "description": "really fun yoga class",
    "day": "2025-05-13",
    "capacity": 50,
    "start_time": "07:00:00",
    "end_time": "08:00:00",
    "instructor": "josephine",
    "room_number": 9
  }
]

GET /classes/:start_time

1. curl -X 'GET' \
  'http://127.0.0.1:3000/classes/start_time/07%3A00%3A00' \
  -H 'accept: application/json' \
  -H 'access_token: brat'

2. [
  {
    "class_name": "yoga flow",
    "class_type": "yoga",
    "description": "really fun yoga class",
    "day": "2025-05-13",
    "capacity": 50,
    "start_time": "07:00:00",
    "end_time": "08:00:00",
    "instructor": "josephine",
    "room_number": 9
  }
]

POST /classes/:id/book

1. curl -X 'POST' \
  'http://127.0.0.1:3000/bookings/3/book?username=gymlover1000' \
  -H 'accept: */*' \
  -H 'access_token: brat' \
  -d ''

2. 204	
Successful Response

GET /users/:id/bookings

1. curl -X 'GET' \
  'http://127.0.0.1:3000/bookingsgymlover1000/bookings' \
  -H 'accept: application/json' \
  -H 'access_token: brat'

2. {
  "username": "gymlover1000",
  "bookings": [
    {
      "class_id": 3,
      "class_name": "yoga flow",
      "day": "2025-05-13",
      "start_time": "07:00:00",
      "end_time": "08:00:00",
      "instructor": "josephine",
      "room_number": 9
    }
  ]
}

# Flow 3: Instructor Sets Up a New Yoga Class

Daniel, a certified instructor, logs into the gym's admin dashboard. He wants to add a new Yoga class to the schedule. First, he checks room availability using the GET /rooms endpoint. He identifies Room 3 as a yoga room. He then creates the new Yoga class using the POST /classes endpoint, naming it “hot yoga”, assigning it to Room 3, and setting the instructor as himself. To verify that the class was added successfully, he retrieves it by name using GET /classes/yoga. He then checks how many classes he has signed up to teach using GET /classes/:instructor to see his week’s schedule.


GET /rooms/rooms

1. curl -X 'GET' \
  'http://127.0.0.1:3000/rooms/rooms' \
  -H 'accept: application/json' \
  -H 'access_token: brat'

2. [
  {
    "number": 1,
    "capacity": 10,
    "type": "cycling"
  },
  {
    "number": 2,
    "capacity": 20,
    "type": "cycling"
  },
  {
    "number": 3,
    "capacity": 30,
    "type": "yoga"
  }
]

POST /classes/

1. curl -X 'POST' \
  'http://127.0.0.1:3000/classes/' \
  -H 'accept: */*' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d ' {
    "class_name": "hot yoga",
    "class_type": "yoga",
    "description": "yoga class but hot",
    "day": "2025-05-13",
    "capacity": 10,
    "start_time": "11:00:00",
    "end_time": "12:00:00",
    "instructor": "Daniel",
    "room_number": 3
  }

2. 204	
Successful Response

GET /classes/:class_name

1. 'curl -X 'GET' \
  'http://127.0.0.1:3000/classes/name/hot yoga' \
  -H 'accept: application/json' \
  -H 'access_token: brat'

2. [
  {
   "class_name": "hot yoga",
    "class_type": "yoga",
    "description": "yoga class but hot",
    "day": "2025-05-13",
    "capacity": 10,
    "start_time": "11:00:00",
    "end_time": "12:00:00",
    "instructor": "Daniel",
    "room_number": 3
  },
  {
    "class_name": "hot yoga",
    "class_type": "yoga",
    "description": "yoga class but hot",
    "day": "2025-05-17",
    "capacity": 8,
    "start_time": "16:00:00",
    "end_time": "17:00:00",
    "instructor": "John",
    "room_number": 15
  }
]

GET /classes/:instructor

1. curl -X 'GET' \
  'http://127.0.0.1:3000/classes/instructor/Daniel' \
  -H 'accept: application/json' \
  -H 'access_token: brat'

2. [
   {
   "class_name": "hot yoga",
    "class_type": "yoga",
    "description": "yoga class but hot",
    "day": "2025-05-13",
    "capacity": 10,
    "start_time": "11:00:00",
    "end_time": "12:00:00",
    "instructor": "Daniel",
    "room_number": 3
  },
{
    "class_name": "breakaway",
    "class_type": "cardio",
    "description": "break a sweat with music",
    "day": "2025-05-15",
    "capacity": 10,
    "start_time": "16:00:00",
    "end_time": "17:00:00.",
    "instructor": "Daniel",
    "room_number": 20
  },
{
    "class_name": "cycling",
    "class_type": "cardio",
    "description": "cycling with music",
    "day": "2025-05-17",
    "capacity": 15,
    "start_time": "11:00:00",
    "end_time": "12:00:00.",
    "instructor": "Daniel",
    "room_number": 4
  }
]

Flow 4
Bob wants to look up a certain class and he only knows the id he uses GET /classes/id/{class_id}, he also wants to look up the room based on the class he was looking up so he gets the room_number from the results before and then does GET /rooms/rooms/:number. This makes him curious about all the rooms so he does GET /rooms/rooms

GET /classes/id/{class_id}
curl -X 'GET' \
  'http://127.0.0.1:3000/classes/id/1' \
  -H 'accept: application/json' \
  -H 'access_token: Brat'
[
   {
   "class_name": "hot yoga",
    "class_type": "yoga",
    "description": "yoga class but hot",
    "day": "2025-05-13",
    "capacity": 10,
    "start_time": "11:00:00",
    "end_time": "12:00:00",
    "instructor": "Daniel",
    "room_number": 3
  },

GET /rooms/rooms/:number
curl -X 'GET' \
  'http://127.0.0.1:3000/rooms/rooms/:number?number=1' \
  -H 'accept: application/json'

[
  {
    "number": 3,
    "capacity": 10,
    "type": "mats"
  }
]

GET /rooms/rooms
curl -X 'GET' \
  'http://127.0.0.1:3000/rooms/rooms' \
  -H 'accept: application/json' \
  -H 'access_token: Brat'

[
  {
    "number": 3,
    "capacity": 10,
    "type": "mats"
  },
  {
    "number": 5,
    "capacity": 25,
    "type": "bikes"
  },
  {
    "number": 6,
    "capacity": 5,
    "type": "reformer"
  }
]


