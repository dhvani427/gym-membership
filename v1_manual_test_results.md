# Flow 1: User Booking a Class
Sophie signs up for the gym using the POST /users/users/register endpoint. Once her account is created, she checks her profile details with the GET /users/users/sophie123 endpoint to confirm the successful registration. Next, she looks at the available membership options through the GET /membership/membership/plans endpoint, picks the one she wants, and then enrolls using POST /membership/membership/sophie123/enroll. 

POST /users/users/register

1. curl -X 'POST' \
  'https://fithub-gym-02nz.onrender.com/users/users/register' \
  -H 'accept: */*' \
  -H 'access_token: PushCodePullWeights' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "sophie123",
  "password": "securePassword123",
  "date_of_birth": "1995-07-15",
  "first_name": "Sophie",
  "last_name": "Smith",
  "email": "sophie.smith@example.com"
}'

2. 204 Successful Response

GET /users/users/sophie123

1. curl -X 'GET' \
  'https://fithub-gym-02nz.onrender.com/users/users/sophie123' \
  -H 'accept: application/json' \
  -H 'access_token: PushCodePullWeights'

2. {
  "username": "sophie123",
  "date_of_birth": "1995-07-15",
  "first_name": "Sophie",
  "last_name": "Smith",
  "email": "sophie.smith@example.com"
}

GET /membership/membership/plans

1. curl -X 'GET' \
  'https://fithub-gym-02nz.onrender.com/membership/membership/plans' \
  -H 'accept: application/json' \
  -H 'access_token: PushCodePullWeights'

2. [
  {
    "membership_id": 1,
    "membership_plan": "basic",
    "cost": 100,
    "max_classes": 10
  },
  {
    "membership_id": 2,
    "membership_plan": "premium",
    "cost": 2000,
    "max_classes": 30
  }
]

POST /membership/membership/sophie123/enroll

1. 
