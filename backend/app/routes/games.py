from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy.sql import func

from ..models import Game, GameSession
from ..database import get_db

router = APIRouter(prefix="/games", tags=["Games"])


# Request validation schemas
class GameCreate(BaseModel):
    title: str

@router.post("/", response_model=dict)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    try:
        new_game = Game(title=game.title)
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        return {"id": new_game.id, "title": new_game.title, "status": new_game.status}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: " + str(e))

@router.get("/", response_model=list)
def get_games(db: Session = Depends(get_db)):    
    # Get active players count for each game
    active_players_subquery = (
        db.query(GameSession.game_id, func.count(GameSession.contestant_id).label("active_players"))
        .filter(GameSession.exited_at == None)  # Players still in the game
        .group_by(GameSession.game_id)
        .subquery()
    )
    
    games_with_active_players = (
        db.query(Game, active_players_subquery.c.active_players)
        .outerjoin(active_players_subquery, Game.id == active_players_subquery.c.game_id)
        .all()
    )
    
    def sort_key(game_with_players):
        game, active_players = game_with_players
        status_priority = {"started": 0, "pending": 1, "ended": 2}
        return (status_priority.get(game.status, 3), active_players or 0)

    
    sorted_games = sorted(games_with_active_players, key=sort_key)
    
    return [
        {
            "id": game.id,
            "title": game.title,
            "status": game.status,
            "active_players": active_players or 0
        }
        for game, active_players in sorted_games
    ]

@router.put("/{game_id}/start")
def start_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.status != "pending":
        raise HTTPException(status_code=400, detail="Game already started or ended")
    game.status = "started"
    game.started_at = datetime.utcnow()
    db.commit()
    return {"message": "Game started"}

@router.put("/{game_id}/end")
def end_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.status != "started":
        raise HTTPException(status_code=400, detail="Game not in progress")
    game.status = "ended"
    game.ended_at = datetime.utcnow()
    db.commit()
    return {"message": "Game ended"}



@router.get("/{game_id}/details")
def get_game_details(game_id: int, db: Session = Depends(get_db)):
    """Get game details, popularity metrics (w1 to w5), and popularity index."""

    # Get game details
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Get the timestamps for yesterday
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    # Calculate w1: Number of people who played the game yesterday
    w1 = (
        db.query(GameSession.contestant_id)
        .filter(GameSession.game_id == game_id)
        .filter(func.date(GameSession.joined_at) == yesterday)
        .distinct()
        .count()
    )

    # Calculate w2: Number of people playing the game right now
    w2 = (
        db.query(GameSession.contestant_id)
        .filter(GameSession.game_id == game_id)
        .filter(GameSession.exited_at == None)  # Players still in the game
        .count()
    )

    # Calculate w3: Total number of upvotes received for the game
    w3 = (
        db.query(func.sum(GameSession.upvotes))
        .filter(GameSession.game_id == game_id)
        .scalar() or 0
    )

    # Calculate w4: Maximum session length of the game played yesterday
    max_session_length = (
        db.query(func.max(GameSession.exited_at - GameSession.joined_at))
        .filter(GameSession.game_id == game_id)
        .filter(func.date(GameSession.joined_at) == yesterday)
        .scalar()
    )
    w4 = max_session_length.total_seconds() if max_session_length else 0

    # Calculate w5: Total number of sessions played yesterday
    w5 = (
        db.query(GameSession.id)
        .filter(GameSession.game_id == game_id)
        .filter(func.date(GameSession.joined_at) == yesterday)
        .count()
    )

    # Subquery to get player count per game for normalization
    subquery_w1 = db.query(GameSession.game_id, func.count(GameSession.contestant_id).label("player_count"))\
        .group_by(GameSession.game_id).subquery()

    subquery_w2 = db.query(GameSession.game_id, func.count(GameSession.contestant_id).label("current_players"))\
        .filter(GameSession.exited_at == None).group_by(GameSession.game_id).subquery()

    subquery_w3 = db.query(GameSession.game_id, func.sum(GameSession.upvotes).label("total_upvotes"))\
        .group_by(GameSession.game_id).subquery()

    subquery_w4 = db.query(GameSession.game_id, func.max(GameSession.exited_at - GameSession.joined_at).label("max_session"))\
        .group_by(GameSession.game_id).subquery()

    subquery_w5 = db.query(GameSession.game_id, func.count(GameSession.id).label("session_count"))\
        .group_by(GameSession.game_id).subquery()

    # Get max values from the subqueries
    max_w1 = db.query(func.max(subquery_w1.c.player_count)).scalar() or 1
    max_w2 = db.query(func.max(subquery_w2.c.current_players)).scalar() or 1
    max_w3 = db.query(func.max(subquery_w3.c.total_upvotes)).scalar() or 1
    max_w4 = db.query(func.max(subquery_w4.c.max_session)).scalar() or timedelta(seconds=1)
    max_w5 = db.query(func.max(subquery_w5.c.session_count)).scalar() or 1

    # Convert max_w4 to seconds (avoid division by zero)
    max_w4 = max_w4.total_seconds() if isinstance(max_w4, timedelta) else max_w4

    # Compute the popularity score
    popularity_index = (
        (0.3 * (w1 / max_w1)) +
        (0.2 * (w2 / max_w2)) +
        (0.25 * (w3 / max_w3)) +
        (0.15 * (w4 / max_w4)) +
        (0.1 * (w5 / max_w5))
    )

    return {
        "game_id": game.id,
        "title": game.title,
        "status": game.status,
        "started_at": game.started_at,
        "ended_at": game.ended_at,
        "w1": w1,
        "w2": w2,
        "w3": w3,
        "w4": w4,
        "w5": w5,
        "popularity_index": round(popularity_index, 4)  # Round for better readability
    }
