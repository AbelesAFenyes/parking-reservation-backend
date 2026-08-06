from fastapi import APIRouter, Depends, status
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

# 204_NO_CONTENT is the universal internet code for "I successfully deleted it, and I have nothing else to say."
@router.delete("/reservations/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation_service.cancel_reservation(db, reservation_id)
    # A 204 response doesn't need to return any data, just a blank screen of success.
    return