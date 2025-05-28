# Case 1: Dirty Read

A gym admin is in the process of creating a new membership plan called "Elite", but the transaction hasn't committed yet. At the same time, a new gym member sends a request to see all membership plans. Since the new plan is written to the database but not committed, it still shows up in the read, which is a dirty read. This is because the uncommitted plan might be rolled back later.

## Sequence Diagram

```mermaid
sequenceDiagram
title Dirty Read

participant Admin  
participant Gym Member  
participant DB  

Note over Admin: Admin starts creating a new "Elite" plan  
Admin->>DB: Create "Elite" plan (not yet committed)  

Note over Gym Member: Member requests to view available plans  
Gym Member->>DB: Read all membership plans  
DB-->>Gym Member: Returns all plans, including uncommitted "Elite"  

Note over Admin: Transaction might still be rolled back  
Note over DB: "Elite" was visible before commit which is a dirty read  
```

## Solution

To prevent the dirty read problem where a user might see a membership plan that hasn’t been committed yet, our API can use the READ COMMITTED isolation level. This means:

While POST /membership transaction is still in progress (uncommitted), a simultaneous GET /membership/plans request from another user will not see the uncommitted plan.
If the admin's transaction is rolled back, the inserted plan is not visible to the gym member.
Only if the transaction is committed successfully will future GET requests include the new plan.

This isolation level prevents users from viewing in-progress or potentially rolled-back changes to the membership plans.

# Case 2: Lost Update

Two gym users, Sophia and Jake, both try to book the last available seat for a Yoga Class at the gym. Both see the same seat as available and proceed to book it simultaneously. Both bookings are processed, causing both to believe they secured the same seat. However, only one seat was available.

## Sequence Diagram

```mermaid
sequenceDiagram
    title Lost Update

    participant Sophia
    participant Jake
    participant DB

    Note over Sophia: Sophia tries to book a spot for a yoga class
    Sophia->>DB: Read booking count (9 booked, 10 capacity)

    Note over Jake: Jake tries to book the same spot at the same time
    Jake->>DB: Read booking count (9 booked, 10 capacity)

    Note over DB: Both see 1 spot left and proceed

    Sophia->>DB: Insert booking
    Jake->>DB: Insert booking

    Note over DB: 11 bookings now exist for 10 spots
```

## Solution

To prevent the lost update problem where two users can book the last seat simultaneously, our API can utilize Optimistic Concurrency Control, where each class booking record includes a row version/timestamp that tracks changes. So, when Sophia or Jake attempts to book the class:

- The current booking count and version number are read.
- The expected version is compared against the actual version at the time of booking.
- If the version has changed (which means another booking happened concurrently), the transaction is rolled back and retried, which ensures that only one user can secure the final spot.
- If no conflict is found, the booking gets committed, and the class version is incremented.

This allows only one booking for the last spot, preventing overbooking.

# Case 3: Read Skew

Instructor A wants to schedule a class from 10:00 AM to 11:00 AM. The system checks if the room is free by querying all existing bookings for that day. While this check is in progress, Instructor B books a class from 10:30 AM to 11:30 AM in the same room and commits the transaction. Instructor A’s transaction doesn’t see this new booking (since it happened after their read) and thinks the room is free for the whole hour so now the schedule overlaps.  

## Sequence Diagram

```mermaid
sequenceDiagram
    title Read Skew

    participant Instructor A
    participant Instructor B
    participant DB

    Note over Instructor A: Instructor A checks if room is free from 10AM to 11AM
    Instructor A->>DB: Read current bookings (no conflict found)

    Note over Instructor B: Instructor B books the same room from 10:30AM to 11:30AM concurrently
    Instructor B->>DB: Insert booking for Instructor B and commit

    Note over Instructor A: Unaware of new booking, Instructor A proceeds to reserve 10AM-11AM
    Instructor A->>DB: Insert booking for Instructor A

    Note over DB: Overlapping bookings now exist
```
## Solution

To prevent this read skew, we can enforce the SERIALIZABLE isolation level in the database during availability checks and bookings. This ensures that if another instructor books the room while Instructor A is checking availability, Instructor A’s transaction will either:

- Retry automatically because the data it relied on became outdated
- Fail, forcing it to recheck availability before proceeding

Alternatively, we can combine the availability check and booking into a single transaction. This way, the system re-verifies availability right before booking. If there’s now a conflict (like Instructor B’s new class), the booking won’t go through, which prevents overlapping classes based on outdated room data.
