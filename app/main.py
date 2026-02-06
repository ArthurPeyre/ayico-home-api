from fastapi import FastAPI
from .routers import users
from .database import Base, engine

# Créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is running!"}

app.include_router(users.router)
