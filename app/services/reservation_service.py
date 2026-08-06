from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import Reservation, ParkingSpot
from app.schemas.schemas import ReservationCreate


def create_reservation(db: Session, reservation_data: ReservationCreate):
    # Rule 1: The user can't travel back in time or end before they start
    if reservation_data.end_time <= reservation_data.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The end time must be after the start time."
        )

    # Rule 2: The parking spot actually has to exist
    spot = db.query(ParkingSpot).filter(ParkingSpot.id == reservation_data.spot_id).first()
    if not spot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking spot not found."
        )

    # Rule 3: The Hitbox Collision (Overlap Check)
    overlapping_reservation = db.query(Reservation).filter(
        Reservation.spot_id == reservation_data.spot_id,
        Reservation.start_time < reservation_data.end_time,
        Reservation.end_time > reservation_data.start_time
    ).first()

    if overlapping_reservation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This parking spot is already booked for the requested time."
        )

    # If it passes all rules, save the new reservation to the database
    new_reservation = Reservation(
        spot_id=reservation_data.spot_id,
        license_plate=reservation_data.license_plate,
        start_time=reservation_data.start_time,
        end_time=reservation_data.end_time
    )

    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return new_reservation