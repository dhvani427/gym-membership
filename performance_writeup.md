### Fake Data Modeling

**Users (50,000):**  
A good approximation for a growing gym brand with several branches.

**Rooms (50):**  
Enough to support a wide variety of equipment types, capacities, and specialized spaces.

**Memberships (50):**  
Supports a wide range of plans — different classes, pool access, VIP options, private rooms, etc.

**Classes (1,900):**  
Covers many types (yoga, abs, pilates, spin) with different instructors, time slots, difficulty levels, and capacities.

**Waitlist (10,000):**  
On average ~10 people waitlisted per class depending on popularity and demand.

**Bookings (338,000):**  
Users book many classes, creating high volume in the system.

**History (600,000):**  
Not all gym visits are for a class - this includes general workout sessions, which are estimated to be twice as frequent as class bookings.

---

### API Performance Metrics

#### `/users`
- `POST /users/register` — *Elapsed time: 0.013005495071411133 seconds*
- `GET /users/{username}` — *Elapsed time: 0.003950357437133789 seconds*

#### `/membership`
- `GET /membership/` — *Elapsed time: 0.009448051452636719 seconds*
- `POST /membership/{user_id}/enroll` — *Elapsed time: 0.009448051452636719 seconds*
- `GET /membership/plans` — *Elapsed time: 0.0007572174072265625 seconds*

#### `/classes`
- `GET /classes/` — *Elapsed time: 0.013226747512817383 seconds*
- `GET /classes/search` — *Elapsed time: 0.0179288387298584 seconds*

#### `/bookings`
- `POST /bookings/book`
- `DELETE /bookings/{class_id}/cancel` — *Elapsed time: 0.0521090030670166 seconds*
- `GET /bookings/{class_id}/waitlist` — *Elapsed time: 0.011786460876464844 seconds*
- `POST /bookings/{class_id}/waitlist/join` — *Elapsed time: 0.02221822738647461 seconds*
- `GET /bookings/{username}` — *Elapsed time: 0.019140243530273438 seconds*

#### `/checkins`
- `POST /checkins/{user_id}/checkin` — *Elapsed time: 0.016108036041259766 seconds*
- `GET /checkins/{user_id}` — *Elapsed time: 0.02290201187133789 seconds*

#### `/rooms`
- `GET /rooms` — *Elapsed time: 0.008251190185546875 seconds*
- `GET /rooms/{number}` — *Elapsed time: 0.00894784927368164 seconds*
- `GET /rooms/{day}` — *Elapsed time: 0.015492677688598633 seconds*

---

### Sample Data Generation

- `GET /sample_data` — *Elapsed time: 186.74650645256042 seconds*

### Performance Tuning

# Before Optimization:

Slowest Endpoint: `DELETE /bookings/{class_id}/cancel`

We identified the class cancellation endpoint as the slowest. The query that selects the first user from the waitlist was the slower query:

```sql
EXPLAIN ANALYZE
SELECT w.user_id, w.waitlist_position, u.username
FROM waitlist w
JOIN users u ON w.user_id = u.user_id
WHERE w.class_id = 1
ORDER BY w.waitlist_position
LIMIT 1;
```

Result:
Limit  (cost=61.43..61.43 rows=1 width=23) (actual time=3.592..3.593 rows=1 loops=1)
  ->  Sort  (cost=61.43..61.44 rows=5 width=23) (actual time=3.591..3.591 rows=1 loops=1)
        Sort Key: w.waitlist_position
        Sort Method: top-N heapsort  Memory: 25kB
        ->  Nested Loop  (cost=4.61..61.40 rows=5 width=23) (actual time=1.398..2.776 rows=5 loops=1)
              ->  Bitmap Heap Scan on waitlist w ...
              ->  Index Scan using users_pkey on users u ...
Planning Time: 7.704 ms  
Execution Time: 4.752 ms

# Explanation:

For performance tuning, we identified the slowest endpoint as the class cancellation route, which involves multiple SQL operations including user lookup, booking deletion, and waitlist promotion. We ran EXPLAIN ANALYZE on the slowest query, the one selecting the first user from the waitlist, and found that it was performing a Bitmap Heap Scan followed by a full sort on waitlist_position to retrieve the lowest-ranked waitlisted user. This sort operation, combined with the nested loop join, was contributing to the overall latency. 

The query scanned all rows matching the class_id in the waitlist table before sorting them by waitlist_position, which is inefficient as the waitlist grows in size. Despite the LIMIT 1 clause, the database executed a full sort of all matching rows prior to limiting the output.

# After Optimization

To optimize this, we created a composite index on (class_id, waitlist_position). This index enables the database to efficiently:
- Filter rows by class_id
- Retrieve rows already sorted by waitlist_position

As a result, the database can directly access the lowest waitlist position without performing a full sort, significantly improving query performance.

```sql
CREATE INDEX idx_waitlist_class_position ON waitlist(class_id, waitlist_position);
```

```sql
EXPLAIN ANALYZE
SELECT w.user_id, w.waitlist_position, u.username
FROM waitlist w
JOIN users u ON w.user_id = u.user_id
WHERE w.class_id = 1
ORDER BY w.waitlist_position
LIMIT 1;
```

Result:
Limit  (cost=0.57..13.64 rows=1 width=23) (actual time=0.784..0.785 rows=1 loops=1)
  ->  Nested Loop  (cost=0.57..65.91 rows=5 width=23) (actual time=0.783..0.783 rows=1 loops=1)
        ->  Index Scan using idx_waitlist_class_position on waitlist w  (cost=0.29..24.37 rows=5 width=8) (actual time=0.700..0.701 rows=1 loops=1)
              Index Cond: (class_id = 1)
        ->  Index Scan using users_pkey on users u  (cost=0.29..8.31 rows=1 width=19) (actual time=0.072..0.072 rows=1 loops=1)
              Index Cond: (user_id = w.user_id)
Planning Time: 4.934 ms
Execution Time: 0.905 ms

# Explanation:
After creating the index on (class_id, waitlist_position), I reran EXPLAIN ANALYZE on the same query. This time, the output showed that PostgreSQL used an Index Scan on idx_waitlist_class_position, which means it was able to directly look up the correct rows in the right order without needing to sort them first.

Before: 4.75 ms (with sort and bitmap heap scan)
After: 0.9 ms (with index scan and no sort)

The composite index on (class_id, waitlist_position) made the query faster because it helps the database quickly find all waitlist entries for a specific class already sorted by their position. This means the database doesn’t have to look through the whole table or do extra sorting after getting the data. Instead, it can jump straight to the first waitlist entry it needs, which makes the query run much faster

