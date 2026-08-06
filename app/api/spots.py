from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.models import ParkingSpot
from app.schemas.schemas import ParkingSpotResponse

# This creates a mini-application for routing our spot-related traffic
router = APIRouter()

@router.get("/spots", response_model=List[ParkingSpotResponse])
def get_all_spots(db: Session = Depends(get_db)):
    # This simply asks the database for every single parking spot and returns them
    spots = db.query(ParkingSpot).all()
    return spots