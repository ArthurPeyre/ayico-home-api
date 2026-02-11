from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Configuration de l'algorithme de hachage (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- FONCTIONS POUR LE MOT DE PASSE ---

def get_password_hash(password: str) -> str:
    """Transforme un mot de passe clair en hash sécurisé"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si le mot de passe clair correspond au hash en base"""
    return pwd_context.verify(plain_password, hashed_password)

# --- FONCTIONS POUR LE TOKEN JWT ---

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
