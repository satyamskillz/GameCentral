from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Contestant
from pydantic import BaseModel

router = APIRouter(prefix="/contestants", tags=["Contestants"])

# Pydantic schema for request validation
class ContestantCreate(BaseModel):
    name: str

@router.post("/create", response_model=dict)
def create_contestant(contestant: ContestantCreate, db: Session = Depends(get_db)):
    new_contestant = Contestant(name=contestant.name)
    db.add(new_contestant)
    db.commit()
    db.refresh(new_contestant)
    return {"id": new_contestant.id, "name": new_contestant.name}

@router.get("/")
def get_contestants(db: Session = Depends(get_db)):
    return db.query(Contestant).all()

@router.get("/{contestant_id}")
def get_contestant(contestant_id: int, db: Session = Depends(get_db)):
    contestant = db.query(Contestant).filter(Contestant.id == contestant_id).first()
    if not contestant:
        raise HTTPException(status_code=404, detail="Contestant not found")
    return contestant

@router.delete("/{contestant_id}")
def delete_contestant(contestant_id: int, db: Session = Depends(get_db)):
    contestant = db.query(Contestant).filter(Contestant.id == contestant_id).first()
    if not contestant:
        raise HTTPException(status_code=404, detail="Contestant not found")
    db.delete(contestant)
    db.commit()
    return {"message": "Contestant deleted successfully"}

@router.put("/{contestant_id}", response_model=dict)
def update_contestant(contestant_id: int, contestant: ContestantCreate, db: Session = Depends(get_db)):
    existing_contestant = db.query(Contestant).filter(Contestant.id == contestant_id).first()
    if not existing_contestant:
        raise HTTPException(status_code=404, detail="Contestant not found")
    existing_contestant.name = contestant.name
    db.commit()
    db.refresh(existing_contestant)
    return {"id": existing_contestant.id, "name": existing_contestant.name}