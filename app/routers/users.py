from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(prefix="/users")

@router.get("/")
def get_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()

@router.post("/")
def create_user(name: str, email: str, db: Session = Depends(database.get_db)):
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
