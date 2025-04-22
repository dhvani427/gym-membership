# 🏋️ Gym Membership API Documentation

## 📌 Endpoints

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
  "success": true
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
    "date": "YYYY-MM-DD",
    "instructor": "string",
    "duration": "integer",
    "difficulty": "string"
  },
  {
    "class_id": "string",
    "class_name": "string",
    "date": "YYYY-MM-DD",
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
    "date": "YYYY-MM-DD",
    "instructor": "string",
    "duration": "integer",
    "difficulty": "string"
  },
  {
    "class": "string",
    "date": "YYYY-MM-DD",
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
    "membership_id": 1,
    "name": "string",
    "price": 99,
    "duration_months": 3
  },
  {
    "membership_id": 2,
    "name": "string",
    "price": 199,
    "duration_months": 6
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
  "success": true
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
  "success": true
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
  "success": true
}
```

---
