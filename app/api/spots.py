from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.models import ParkingSpot
from app.schemas.schemas import ParkingSpotResponse, ReservationResponse
from app.services import reservation_service

# This creates a mini-application for routing our spot-related traffic
router = APIRouter()

@router.get("/spots", response_model=List[ParkingSpotResponse])
def get_all_spots(db: Session = Depends(get_db)):
    # This simply asks the database for every single parking spot and returns them
    spots = db.query(ParkingSpot).all()
    return spots

# The {spot_id} in the URL is a variable. If the user goes to /spots/5/reservations, spot_id becomes 5.
@router.get("/spots/{spot_id}/reservations", response_model=List[ReservationResponse])
def get_spot_reservations(spot_id: int, db: Session = Depends(get_db)):
    return reservation_service.get_reservations_for_spot(db, spot_id)