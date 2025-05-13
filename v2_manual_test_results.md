# Flow 2: Flow 2: User Books Yoga Class

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

