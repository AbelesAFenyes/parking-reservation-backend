from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.schemas import ReservationCreate, ReservationResponse
from app.services import reservation_service

router = APIRouter()

# status_code=201 means "Successfully Created"
@router.post("/reservations", response_model=ReservationResponse, status_code=201)
def make_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    # We just hand the request over to the brain we built in step 2!
    return reservation_service.create_reservation(db, reservation)