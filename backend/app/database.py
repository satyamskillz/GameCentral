# database.py: Sets up the connection to PostgreSQL using SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()


# PostgreSQL connection string using the Docker Compose service name "db"
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an SQLAlchemy engine to manage connections
engine = create_engine(DATABASE_URL)

# Configure a session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our SQLAlchemy models
Base = declarative_base()

# Dependency that provides a database session for each request in FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide the session to the request
    finally:
        db.close()  # Ensure the session is closed after the request is done
