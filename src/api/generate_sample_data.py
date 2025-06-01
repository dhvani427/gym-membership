from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

import sqlalchemy
from src.api import auth
from src import database as db
from datetime import date, time
from src.database import engine

import os
import dotenv
from faker import Faker
import numpy as np
from datetime import datetime, timedelta, time

router = APIRouter(
    prefix="/sample_data",
    tags=["sample_data"],
    dependencies=[Depends(auth.get_api_key)],
)

fake = Faker()

def random_time(start_hour=6, end_hour=22):
    # Random time between start_hour and end_hour
    hour = np.random.randint(start_hour, end_hour)
    minute = np.random.choice([0, 15, 30, 45])
    return time(hour, minute)

def random_date(start_days_ago=365):
    # Random date within the last year
    return datetime.now().date() - timedelta(days=np.random.randint(0, start_days_ago))

@router.post("", status_code=status.HTTP_204_NO_CONTENT)
def generate_sample_data():
    with engine.begin() as conn:
        conn.execute(sqlalchemy.text("""
        DROP TABLE IF EXISTS bookings;
        DROP TABLE IF EXISTS history;
        DROP TABLE IF EXISTS waitlist;
        DROP TABLE IF EXISTS classes;
        DROP TABLE IF EXISTS rooms;
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS membership;
                                     
        CREATE TABLE rooms (
            room_number int not null PRIMARY KEY,
            capacity int not null,
            type text not null
        );
                                     
        CREATE TABLE classes (
            class_id int generated always as identity not null PRIMARY KEY,
            class_name text not null,
            class_type text not null,
            description text not null,
            day date not null,
            capacity int not null,
            start_time time not null,
            end_time time not null,
            instructor text not null,
            room_number int not null references rooms(room_number)
        );

        CREATE TABLE membership (
            membership_id int generated always as identity not null PRIMARY KEY,
            membership_plan text not null unique,
            cost int not null,
            max_classes int not null
        );
                                     
        CREATE TABLE users (
            user_id int generated always as identity not null PRIMARY KEY,
            username text not null unique,
            first_name text not null,
            last_name text not null,
            email text not null,
            date_of_birth date not null,
            password text not null,
            membership int null references membership(membership_id)
        );
                                                                                             
        CREATE TABLE waitlist (
            class_id int not null,
            user_id int not null,
            waitlist_position int not null,
            PRIMARY KEY (class_id, user_id),
            FOREIGN KEY (class_id) REFERENCES classes(class_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE history (
            history_id int generated always as identity not null PRIMARY KEY,
            check_in_date date not null,
            check_in_time time not null,
            user_id int not null references users(user_id)
        );

        CREATE TABLE bookings (
            booking_id int generated always as identity not null PRIMARY KEY,
            class_id int not null references classes(class_id),
            user_id int not null references users(user_id)
        );
        """))

        # Insert rooms (50)
        print("Populating rooms...")
        room_types = ['Yoga', 'Spin', 'Weights', 'Cardio', 'Dance']
        rooms = [{"room_number": i+1, "capacity": np.random.randint(10, 50), "type": fake.random_element(room_types)} for i in range(50)]
        conn.execute(sqlalchemy.text("""
            INSERT INTO rooms (room_number, capacity, type) VALUES (:room_number, :capacity, :type)
        """), rooms)

        # Insert memberships (50)
        print("Populating membership plans...")
        memberships = []
        for i in range(50):
            memberships.append({
                "membership_plan": f"Plan {i+1}",
                "cost": np.random.randint(30, 200),
                "max_classes": np.random.randint(1, 10)
            })
        conn.execute(sqlalchemy.text("""
            INSERT INTO membership (membership_plan, cost, max_classes) VALUES (:membership_plan, :cost, :max_classes)
        """), memberships)

        # Insert users (50,000)
        print("Populating users...")
        membership_ids = list(range(1, 51))  # membership IDs from 1 to 50
        batch_size = 5000
        total_users = 50000

        for batch_start in range(0, total_users, batch_size):
            users_batch = []
            for i in range(batch_size):
                profile = fake.simple_profile()
                # Append a unique index to username to guarantee uniqueness
                username = profile['username'] + str(batch_start + i)
                
                users_batch.append({
                    "username": username,
                    "first_name": profile['name'].split()[0],
                    "last_name": profile['name'].split()[-1],
                    "email": profile['mail'],
                    "date_of_birth": profile['birthdate'],
                    "password": fake.password(length=10),
                    "membership": fake.random_element(membership_ids)
                })
            conn.execute(sqlalchemy.text("""
                INSERT INTO users (username, first_name, last_name, email, date_of_birth, password, membership)
                VALUES (:username, :first_name, :last_name, :email, :date_of_birth, :password, :membership)
            """), users_batch)
            print(f"Inserted users: {batch_start + batch_size}")

        # Insert classes (1,900)
        print("Populating classes...")
        room_numbers = [r["room_number"] for r in rooms]
        class_types = ['Yoga', 'Spin', 'Weights', 'Cardio', 'Dance']
        instructors = [fake.name() for _ in range(200)]  # pool of instructors' names
        classes = []
        for _ in range(1900):
            day = random_date()
            start = random_time()
            # classes last between 30 mins to 1.5 hours
            duration_minutes = np.random.choice([30, 45, 60, 75, 90])
            end_dt = (datetime.combine(datetime.today(), start) + timedelta(minutes=int(duration_minutes))).time()

            classes.append({
                "class_name": fake.word().title() + " Class",
                "class_type": fake.random_element(class_types),
                "description": fake.text(max_nb_chars=100),
                "day": day,
                "capacity": np.random.randint(10, 50),
                "start_time": start,
                "end_time": end_dt,
                "instructor": fake.random_element(instructors),
                "room_number": fake.random_element(room_numbers)
            })
        conn.execute(sqlalchemy.text("""
            INSERT INTO classes (class_name, class_type, description, day, capacity, start_time, end_time, instructor, room_number)
            VALUES (:class_name, :class_type, :description, :day, :capacity, :start_time, :end_time, :instructor, :room_number)
        """), classes)

        # Insert waitlist (10,000)
        print("Populating waitlist...")
        user_ids = list(range(1, 50001))
        class_ids = list(range(1, 1901))
        waitlist = []
        seen = set()

        while len(waitlist) < 10000:
            entry = {
                "class_id": fake.random_element(class_ids),
                "user_id": fake.random_element(user_ids),
                "waitlist_position": np.random.randint(1, 21)
            }
            key = (entry["class_id"], entry["user_id"])
            if key not in seen:
                seen.add(key)
                waitlist.append(entry)

        conn.execute(sqlalchemy.text("""
            INSERT INTO waitlist (class_id, user_id, waitlist_position)
            VALUES (:class_id, :user_id, :waitlist_position)
        """), waitlist)


        # Insert history (600,000)
        print("Populating history...")
        batch_size = 10000
        for batch_start in range(0, 600000, batch_size):
            history_batch = []
            for _ in range(batch_size):
                history_batch.append({
                    "check_in_date": random_date(),
                    "check_in_time": random_time(),
                    "user_id": fake.random_element(user_ids)
                })
            conn.execute(sqlalchemy.text("""
                INSERT INTO history (check_in_date, check_in_time, user_id)
                VALUES (:check_in_date, :check_in_time, :user_id)
            """), history_batch)
            print(f"Inserted history: {batch_start + batch_size}")

        # Insert bookings (338,000)
        print("Populating bookings...")
        batch_size = 10000
        for batch_start in range(0, 338000, batch_size):
            bookings_batch = []
            for _ in range(batch_size):
                bookings_batch.append({
                    "class_id": fake.random_element(class_ids),
                    "user_id": fake.random_element(user_ids)
                })
            conn.execute(sqlalchemy.text("""
                INSERT INTO bookings (class_id, user_id)
                VALUES (:class_id, :user_id)
            """), bookings_batch)
            print(f"Inserted bookings: {batch_start + batch_size}")

        print("Data population complete!")
