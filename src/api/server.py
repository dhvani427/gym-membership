from fastapi import FastAPI
from src.api import users, membership, classes, bookings, checkins, rooms
from starlette.middleware.cors import CORSMiddleware

description = """
Push Code 💻, Pull Weights 🏋️"""

tags_metadata = [
    {"name": "users", "description": "Manage gym users"},
    {"name": "membership", "description": "Membership plans and status"},
    {"name": "classes", "description": "Fitness class schedules"},
    {"name": "bookings", "description": "Class bookings"},
    {"name": "checkins", "description": "Gym check-in logs"},
    {"name": "rooms", "description": "Room and facility management"},
]

app = FastAPI(
    title="FitHub",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Dhvani Goel",
        "email": "dhgoel@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)

origins = ["https://potion-exchange.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(membership.router)
app.include_router(classes.router)
app.include_router(bookings.router)
app.include_router(checkins.router)
app.include_router(rooms.router)
#app.include_router(generate_sample_data.router)


@app.get("/")
async def root():
    return {"message": "Welcome to our Gym - FitHub!"}
