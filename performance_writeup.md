### Fake Data Modeling

**Users (50,000):** A good approximation for a growing gym brand with several branches.
**Rooms (50):** Enough to support a wide variety of equipment types, capacities, and specialized spaces.
**Memberships (50):** Supports a wide range of plans — different classes, pool access, VIP options, private rooms, etc.
**Classes (1,900):** Covers many types (yoga, abs, pilates, spin) with different instructors, time slots, difficulty levels, and capacities.
**Waitlist (10,000):** On average ~10 people waitlisted per class depending on popularity and demand.
**Bookings (338,000):** Users book many classes, creating high volume in the system.
**History (600,000):** Not all gym visits are for a class - this includes general workout sessions, which are estimated to be twice as frequent as class bookings.

/users/register
- Elapsed time: 0.013005495071411133 seconds
/users/{username}
- Elapsed time: 0.003950357437133789 seconds

/membership/
- Elapsed time: 0.009448051452636719 seconds
/membership/{user_id}/enroll
- Elapsed time: 0.009448051452636719 seconds
/membership/plans
- Elapsed time: 0.0007572174072265625 seconds

/classes/
- Elapsed time: 0.013226747512817383 seconds
/classes/search
- Elapsed time: 0.0179288387298584 seconds

/bookings/book
/bookings/{class_id}/cancel
- Elapsed time: 0.0521090030670166 seconds
/bookings/{class_id}/waitlist
- Elapsed time: 0.011786460876464844 seconds
/bookings/{class_id}/waitlist/join
- Elapsed time: 0.02221822738647461 seconds
/bookings/{username}
- Elapsed time: 0.019140243530273438 seconds

/checkins/{user_id}/checkin
- Elapsed time: 0.016108036041259766 seconds
/checkins/{user_id}
- Elapsed time: 0.02290201187133789 seconds

/rooms
- Elapsed time: 0.008251190185546875 seconds
/rooms/{number}
- Elapsed time: 0.00894784927368164 seconds
/rooms/{day}
- Elapsed time: 0.015492677688598633 seconds


/sample_data
- Elapsed time: 186.74650645256042 seconds


