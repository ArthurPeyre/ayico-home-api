from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import users
from .database import Base, engine

# Créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

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

app.include_router(users.router)
