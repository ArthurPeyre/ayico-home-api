from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas
from ..models import user
from ..core.security import get_password_hash

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[schemas.UserRead])
def get_users(db: Session = Depends(database.get_db)):
    return db.query(user.User).all()

@router.post("/", response_model=schemas.UserRead)
def create_user(newUser: schemas.UserCreate, db: Session = Depends(database.get_db)):

    existing_user = db.query(user.User).filter(user.User.email == newUser.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = user.User(
        name=newUser.name,
        email=newUser.email,
        hashed_password=get_password_hash(newUser.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
