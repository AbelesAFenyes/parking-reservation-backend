from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine, Base, SessionLocal
from app.db.seed import seed_data
from app.api import spots  # <-- IMPORT YOUR NEW ROUTER

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
    yield

app = FastAPI(lifespan=lifespan, title="Parking Reservation API")

# <-- HOOK UP THE ROUTER HERE
app.include_router(spots.router, prefix="/api/v1", tags=["Parking Spots"])

@app.get("/")
def read_root():
    return {"message": "Parking API is running!"}