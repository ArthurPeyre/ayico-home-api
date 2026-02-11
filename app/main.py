from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import users, auth
from .database import Base, engine

# Système de retry pour la connexion à la DB
retries = 5
while retries > 0:
    try:
        Base.metadata.create_all(bind=engine)
        break
    except OperationalError:
        retries -= 1
        print(f"Attente de la DB... ({retries} essais restants)")
        time.sleep(2)

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://frontend:5173",
        "http://localhost:5173",
        "http://raspberrypi:5173",
        "http://192.168.1.50:5173",
        "http://raspberrypi.local:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, etc.
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API is running!"}

app.include_router(auth.router)
app.include_router(users.router)
