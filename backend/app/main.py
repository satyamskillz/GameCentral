# main.py: FastAPI entry point

from fastapi import FastAPI
from .routes import contestants, games, game_sessions, leaderboard
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Game Leaderboard API", version="1.0")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register route modules
app.include_router(contestants.router)
app.include_router(games.router)
app.include_router(game_sessions.router)
app.include_router(leaderboard.router)

# Root endpoint (optional)
@app.get("/")
def root():
    return {"message": "Welcome to the Game Leaderboard API!", "debug": os.getenv("DEBUG")}
