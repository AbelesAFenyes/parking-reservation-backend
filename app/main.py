from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine, Base, SessionLocal
from app.db.seed import seed_data

# This tells SQLAlchemy to look at our blueprints and build the empty tables in the database.
Base.metadata.create_all(bind=engine)


# The lifespan acts as the "opening shift manager" for your app.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # BEFORE the app starts taking requests:
    db = SessionLocal()
    try:
        seed_data(db)  # Run our stocking script
    finally:
        db.close()  # Throw away the clipboard

    yield  # The app is now "open for business" and waiting for requests

    # (Anything below the yield would run when the app shuts down)


app = FastAPI(lifespan=lifespan, title="Parking Reservation API")


@app.get("/")
def read_root():
    return {"message": "Parking API is running!"}