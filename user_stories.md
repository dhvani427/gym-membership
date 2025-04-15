User Stories

As a gym member, I want to filter fitness classes by category, time of day, and instructor, so that I can quickly book evening HIIT sessions with my preferred trainer without scrolling through irrelevant options.

As a gym admin, I want to create and update class schedules with participant capacity limits, so that I can manage class sizes, prevent double bookings, and ensure each member gets adequate attention.

As a gym member on a basic plan, I want to see only the classes included in my membership tier before booking, so that I don’t waste time trying to register for premium-only sessions I’m not eligible for.

As a gym member, I want to view a detailed history of my past check-ins and class attendance, including dates and class types, so that I can track my progress and stay motivated to reach my fitness goals.

As a trainer, I want to access real-time check-in data for my classes and mark each attendee as present or absent, so that I can maintain accurate attendance records.

As a trainer, I want to cancel or reschedule a class I’m assigned to — with the option to notify all registered members — so that I can manage last-minute schedule changes without causing confusion for attendees.

As a gym member, I want to easily access information about my gym membership online, with the option to view all available plans, so that I can choose the one that best fits my needs.

As a trainer, I want to be able to view the full list of members registered for each of my classes, including their names and membership status, so I can plan ahead by preparing the necessary equipment, adjusting the workout intensity if needed, and setting up the space to accommodate the group size comfortably.

As a gym admin, I want to track daily attendance, check-in logs, and class participation, so I can generate reports, identify popular classes, and make informed decisions about scheduling and services to better meet member preferences.

As a gym member training for competitive bodybuilding shows, I need a way to easily track my progress and workouts. Consistency and a curated routine is essential so being able to easily check my history and show it to my trainor is an essential for me!

As a gym member who has bad experiences with canceling previous gym memberships, I need a way to easily cancel my membership with no tricks. Went to Planet Fitness in the past, huge mistake, they wouldn't let me cancel! Forever traumatized. 

As a gym admin my job is to make sure my customers are happy and everything is running smoothly. Making sure customers have another resource to rely on other than limited phone and operational hours is essential. 




/****************************************************************************************************************************************************************************/


Exceptions

Exception: No classes match the filter criteria
If a gym member filters by category, time of day, and instructor but finds no results, the system will display a message like: “No classes match your filters. Try adjusting your criteria or view all available classes.”

Exception: Class scheduling conflict for an admin
If an admin tries to schedule a class that conflicts with another, the system will show: “This class overlaps with an existing one.” It will suggest adjusting the time or room and provide simple options to change or cancel the conflicting session.

Exception: Basic member tries to access premium-only class
If a basic plan member tries to book a class restricted to premium members, the system will show an alert: “This class is available only for premium members.” The member will be prompted to upgrade their membership or select another class they can attend based on their membership tier.

Exception: User tries to sign up with an account that already exists.
If a user attempts to register using an email address that’s already associated with an existing account, the system will prevent the registration and display a message saying “An account with this email already exists.”

Exception: User books overlapping class accidentally
If a user attempts to book a class that overlaps in time with another class they’ve already signed up for, the system will detect the conflict and block the booking. A message will be shown saying “You already have a class booked during this time,” and the user will be prompted to cancel the existing class or select a different time slot.

Exception: User with a Basic plan tries to book more than 3 classes per week
If a user with a Basic-tier membership attempts to book a fourth class within the same calendar week, the system will prevent the booking and show a message saying “You’ve reached your weekly booking limit for your current plan.” The user will be given the option to upgrade to a higher tier or wait until the next week to book again.

Exception: User attempts to sign up for a class, but the class is at full capacity.
If a user attempts to sign up for a class, but the class is at full capacity, the system will display a message saying: “This class is currently full.” The user will not be able to sign up for the class, and the system will recommend other available classes with open spots.

Exception: User tries to book a class but has overdue payments
If a user attempts to book a class but has an outstanding payment, the system will display a message saying: “You have an outstanding balance. Please make payment.” The user will not be allowed to sign up for the class until a payment is made.

Exception: Trainer tries to delete a class that already has signed-up participants
If a trainer tries to delete a class that already has bookings, the system will display a message: “The class already has participants and cannot be deleted. Cancel instead?” The trainer will be given the option to cancel the class instead, and participants will be notified.

Exception: User tries to book a class outside of allowed cancellation window.
If a user attempts to cancel too close to the class they will be charged a late cancellation fee. For example there could be a 24 hour window and people can’t cancel in that window before the class. This is important because we don’t want to save a spot for someone who isn’t going to show up. Message will be displayed: “Cancellation period has ended. You can no longer cancel this class without a late fee being applied.”

Exception: User tries to book a class outside of allowed booking window
Classes open up [X] days in advance so that people can’t just book up for the whole month, so if someone tries to book before they open they will get a message: “Bookings are only available within [X] days in advance. Please select a valid time.”

Exception: User tires to book a class with an invalid payment method
If the user tries to book a class with an invalid payment method, for example expired credit card, insufficient balance, etc, then the request to book will not go through and a message occurs saying: “Your payment method is invalid. Please update your payment details to proceed with the booking.”
