from fastapi import APIRouter, Response, HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..core.security import verify_password, create_access_token
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Authentication"])

# On crée un petit schéma interne pour la requête de login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(login_data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    # 1. Chercher l'utilisateur par son email
    user = db.query(User).filter(User.email == login_data.email).first()
    
    # 2. Vérifier si l'utilisateur existe ET si le mot de passe est correct
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Créer le token
    token = create_access_token({"sub": str(user.id)})

    # 4. Placer le token dans un cookie HTTP-only (Sécurisé)
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,  # Empêche le JavaScript de lire le cookie (contre XSS)
        secure=False,   # Mets à True quand tu seras en HTTPS
        samesite="lax",
        max_age=1800    # Expire après 30 min (comme ton token)
    )

    return {"message": "Connexion réussie", "user": {"name": user.name, "email": user.email}}
