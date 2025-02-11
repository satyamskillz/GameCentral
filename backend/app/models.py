# models.py: Defines the SQLAlchemy models for the application
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Model for a Contestant in the system
class Contestant(Base):
    __tablename__ = "contestants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)  # Contestant's name
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # When the contestant was created
    
    # Relationship to track game sessions the contestant participates in
    game_sessions = relationship("GameSession", back_populates="contestant", cascade="all, delete-orphan")

# Model for a Game in the system
class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)  # Name or title of the game, must be unique
    status = Column(String, default="pending")  # Game status: pending, started, ended
    started_at = Column(DateTime, nullable=True)  # When the game was started
    ended_at = Column(DateTime, nullable=True)    # When the game was ended
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Game creation timestamp
    
    # Relationship to track contestants in the game via game sessions
    game_sessions = relationship("GameSession", back_populates="game", cascade="all, delete-orphan")


# Model for a GameSession, linking a contestant with a game
class GameSession(Base):
    __tablename__ = "game_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False)  # ID of the related game
    contestant_id = Column(Integer, ForeignKey("contestants.id", ondelete="CASCADE"), nullable=False)  # ID of the related contestant
    joined_at = Column(DateTime, default=datetime.datetime.utcnow)  # When the contestant joined the game
    exited_at = Column(DateTime, nullable=True)  # When the contestant left the game (if applicable)
    score = Column(Float, default=0.0)  # Contestant's score in the game
    upvotes = Column(Integer, default=0)  # Number of upvotes received for the game session
    
    # Establish relationships to Game and Contestant models
    game = relationship("Game", back_populates="game_sessions")
    contestant = relationship("Contestant", back_populates="game_sessions")
