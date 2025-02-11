from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from ..database import get_db
from ..models import GameSession, Contestant

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

@router.get("/")
def get_global_leaderboard(db: Session = Depends(get_db)):
    top_scores = db.query(
        GameSession.contestant_id,
        Contestant.name,
        func.sum(GameSession.score).label("total_score")
    ).join(Contestant, GameSession.contestant_id == Contestant.id).group_by(GameSession.contestant_id, Contestant.name).order_by(func.sum(GameSession.score).desc()).limit(100).all()

    return [{"id": row[0], "name": row[1], "score": row[2]} for row in top_scores]

@router.get("/games/{game_id}")
def get_game_leaderboard(game_id: int, db: Session = Depends(get_db)):
    
    top_scores = db.query(
        GameSession.contestant_id,
        Contestant.name,
        GameSession.score
    ).join(Contestant, GameSession.contestant_id == Contestant.id).filter(GameSession.game_id == game_id).filter(GameSession.exited_at == None).order_by(GameSession.score.desc()).limit(100).all()

    return [{"id": row[0], "name": row[1], "score": row[2]} for row in top_scores]
