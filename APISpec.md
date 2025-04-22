API Documentation

/users/Register: create a new account (POST)

Request: {
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  “email”: “string”,
  “password”: “string”,
  “membership_plan”: “string”,
}

Response: {
“Success”: true,
}

/users/{username} (GET)

Request: {}

Response:  {
  "username": "string",
  "first_name": "string",
  "last_names": "string",
  “email”: “string”,
  “membership_plan”: "string",
}

/classes/{date} (GET)

Request: 
[
  {
    "Class_id": "string",
    “Class_name”: "string"
    "Date": "YYYY-MM-DD",
    "Instructor": "string",
    "Duration": “integer”,
    "Difficulty": “string”
  },
  {
    "Class": "string",
    "Date": "YYYY-MM-DD",
    "Instructor": "string",
    "Duration": “integer”,
    "Difficulty": “string”
  }
]

/users/{username}/bookings (GET)

Request: {}
Response: 
[
  {
    "Class": "string",
    "Date": "date",
    "Instructor": "string",
    "Duration": “int”,
    "Difficulty": “string”
  },
  {
    "Class": "string",
    "Date": "date",
    "Instructor": "string",
    "Duration": “int”,
    "Difficulty": “string”
  }
]

/membership-plans (GET)

Request: {}
Response:
[
  {
    "membership_id": int,
    "name": "string",
    "price": int,
    "duration_months": int
  },
  {
    "membership_id": int,
    "name": "string",
    "price": “integer”,
    "duration_months": int
  }
]

/classes/{class_id}/enroll (POST)

Request: {
  “username”: “string”
}
Response: {}

Add membership to cart
/{cart_id}/carts/{membership_id} (PUT)

Request:
{
	“Membership_id”: “int”
	“Name” : “string”
	“Cost”: “int”
}
Response:
{
	“Success”: “boolean”
}

{cart_id}/checkout (POST)
	Request:
	{
 	"payment": "string",
}
Response:
{
	“Success”: “boolean”
}
