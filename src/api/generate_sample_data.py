from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional


import sqlalchemy
from src.api import auth
from src import database as db
from datetime import date, time
from src.database import engine

router = APIRouter(
    prefix="/sample_data",
    tags=["sample_data"],
    dependencies=[Depends(auth.get_api_key)],
)

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
