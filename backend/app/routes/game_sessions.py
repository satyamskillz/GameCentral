from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import GameSession, Game, Contestant
from pydantic import BaseModel
import datetime

router = APIRouter(prefix="/games", tags=["Game Sessions"])

class JoinGameRequest(BaseModel):
    contestant_id: int

@router.post("/{game_id}/contestants/{contestant_id}/join")
def join_game(game_id: int, contestant_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    contestant = db.query(Contestant).filter(Contestant.id == contestant_id).first()

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if not contestant:
        raise HTTPException(status_code=404, detail="Contestant not found")
    if game.status != "started" or game.ended_at is not None:
        raise HTTPException(status_code=400, detail="Game can not be joined")

    new_session = GameSession(game_id=game_id, contestant_id=contestant_id)
    db.add(new_session)
    db.commit()
    return {"message": "Contestant joined the game"}



@router.put("/{game_id}/contestants/{contestant_id}/score")
def update_score(game_id: int, contestant_id: int, score: float, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter(
        GameSession.game_id == game_id,
        GameSession.contestant_id == contestant_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Contestant not in this game")

    session.score = score
    db.commit()
    return {"message": "Score updated"}

@router.put("/{game_id}/contestants/{contestant_id}/exit")
def exit_game(game_id: int, contestant_id: int, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter(
        GameSession.game_id == game_id,
        GameSession.contestant_id == contestant_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Contestant not in this game")

    session.exited_at = datetime.datetime.utcnow()
    db.commit()
    return {"message": "Contestant exited the game"}
