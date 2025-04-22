Example Flows

Flow 1: User Booking a Class
Maria wants to sign up for a yoga class. She logs in her gym account via POST /users/{username}. Then she checks for available yoga classes GET /classes?type=yoga. She looks through the results and finds a vinyasa flow yoga class she likes with class_id: 101. Then she books a spot in the class with POST /users/{username}/bookings, where class_id is passed as a parameter.

Flow 2: Instructor signing up to run a class
Bob wants to teach spin class this week and monitor the signups. He logs in via POST /users/{username} and creates a new spin class via POST /classes/ with details like class title, timing, room, capacity, and intensity. He then checks who signed up for his class using GET classes/{class_id}/bookings. 

Flow 3: User Canceling a Class
John realizes he can’t attend his booked Yoga class on Thursday morning. So he logs in via POST /users/{username} and checks what classes he had booked through GET users/{username}/bookings. He cancels his class via DELETE /bookings/{class_id}. He gets a successful confirmation that his booking has been canceled, freeing up one spot in the class.

Flow 4: User creates an account and purchases a gym membership plan
Sophie is new to the gym and wants to join as a member. She starts by creating an account using POST /users/register, providing her name, email, password. After registering, she retrieves her profile information using GET /users/sophie123. Next, she adds her chosen membership to her cart using PUT /cart789/carts/2, passing in the cart id and membership id. Then, she completes the purchase by checking out with POST {cart_id}/checkout, providing her payment method.
