from fastapi import APIRouter, Response, HTTPException
from core.security import create_access_token

router = APIRouter()

@router.post("/login")
def login(response: Response):
    # EXEMPLE : utilisateur validé
    user_id = 42

    token = create_access_token({"sub": str(user_id)})

    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        secure=False,   # True en HTTPS
        samesite="lax"
    )

    return {"status": "ok"}
