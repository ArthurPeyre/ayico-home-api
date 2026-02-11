from ..models import user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, schemas

router = APIRouter(prefix="/users")

@router.get("/")
def get_users(db: Session = Depends(database.get_db)):
    return db.query(user.User).all()

@router.post("/")
def create_user(newUser: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = user.User(name=newUser.name, email=newUser.email, hashed_password=newUser)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
