# Gym Membership API Documentation

## Endpoints

---

### **POST /users/Register**  
Create a new user account.

#### Request
```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "password": "string",
  "membership_plan": "string"
}
```

#### Response
```json
{
  "success": "boolean"
}
```

---

### **GET /users/{username}**  
Get a user's profile by username.

#### Request
```json
{}
```

#### Response
```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "membership_plan": "string"
}
```

---

### **GET /classes/{date}**  
Get a list of classes available on a specific date.

#### Request
```json
{}
```

#### Response
```json
[
  {
    "class_id": "string",
    "class_name": "string",
    "date": "date",
    "instructor": "string",
    "duration": "integer",
    "difficulty": "string"
  },
  {
    "class_id": "string",
    "class_name": "string",
    "date": "date",
    "instructor": "string",
    "duration": "integer",
    "difficulty": "string"
  }
]
```

---

### **GET /users/{username}/bookings**  
View all classes booked by a specific user.

#### Request
```json
{}
```

#### Response
```json
[
  {
    "class": "string",
    "date": "date",
    "instructor": "string",
    "duration": "integer",
    "difficulty": "string"
  },
  {
    "class": "string",
    "date": "date",
    "instructor": "string",
    "duration": "integer",
    "difficulty": "string"
  }
]
```

---

### **GET /membership-plans**  
List all available membership plans.

#### Request
```json
{}
```

#### Response
```json
[
  {
    "membership_id": "integer",
    "name": "string",
    "price": "integer",
    "duration_months": "integer"
  },
  {
    "membership_id": "integer",
    "name": "string",
    "price": "integer",
    "duration_months": "integer"
  }
]
```

---

### **POST /classes/{class_id}/enroll**  
Enroll a user in a class.

#### Request
```json
{
  "username": "string"
}
```

#### Response
```json
{
  "success": "boolean"
}
```

---

### **PUT /{cart_id}/carts/{membership_id}**  
Add a membership to the cart.

#### Request
```json
{
  "membership_id": "integer",
  "name": "string",
  "cost": "integer"
}
```

#### Response
```json
{
  "success": "boolean"
}
```

---

### **POST /{cart_id}/checkout**  
Checkout and make a payment.

#### Request
```json
{
  "payment": "string"
}
```

#### Response
```json
{
  "success": "boolean"
}
```
### **POST /checkins/{user_id}/checkin**
Check in a user by inserting a row into the history table.

#### Request
```json
{}
```

#### Response
```json
{
  "success": "boolean"
}
```

### **GET /checkins/users/{user_id}/checkins**
Retrieve a user's check-in history.
### Request
```json
{}
```

#### Response
```json
[
  {
    "check_in_date": "string",
    "check_in_time": "string"
  }
]
```

---

### **GET /rooms/{date}**
Retrieve available rooms based on for a given date.
### Request
```json
{
  "day": "YYYY-MM-DD"
}
```

#### Response
```json
[
  {
    "number": "integer",
    "day": "YYYY-MM-DD",
    "availability_slots": [
      {
        "start": "HH:MM:SS",
        "end": "HH:MM:SS"
      },
      {
        "start": "HH:MM:SS",
        "end": "HH:MM:SS"
      }
    ]
  },
  {
    "number": "integer",
    "day": "YYYY-MM-DD",
    "availability_slots": [
      {
        "start": "HH:MM:SS",
        "end": "HH:MM:SS"
      }
    ]
  }
]

```
---
### **POST /bookings/{class_id}/book**
Retrieve available rooms based on for a given date.
### Request
```json
{
  "username": "string",
  "class_id": "integer"
}
```

#### Response
```json
{
  "class_id": "integer",
  "enrollment_status": "string"  //"Booking successful" or "Class is full, please join the waitlist or choose another class"
}
```

### **POST /bookings/{class_id}/waitlist/join**
Add a user to the waitlist for a class.
### Request
```json
{
  "username": "string",
  "class_id": "integer"
}
```

#### Response
```json
{
  "username": "string",
  "class_id": "integer",
  "waitlist_position": "integer"
}
```

### **GET /bookings/{class_id}/waitlist**
Retrieve the waitlist for a specific class.
### Request
```json
{
  "class_id": "integer"
}
```

#### Response
```json
{
  "class_id": "integer",
  "waitlist": [
    {
      "username": "string",
      "waitlist_position": "integer"
    },
    ...
  ]
}
```

### **DELETE /bookings/{class_id}/cancel**
Cancel a user's booking for a class. If there are users on the waitlist, the first one is enrolled automatically.
### Request
```json
{
  "username": "string",
  "class_id": "integer"
}
```

#### Response
```json
{
  "class_id": "integer",
  "cancellation_status": "string",
  "enrolled_from_waitlist": "string"
}
```
