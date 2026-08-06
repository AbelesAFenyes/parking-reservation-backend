from sqlalchemy.orm import Session
from app.models.models import ParkingSpot, SpotType


def seed_data(db: Session):
    # Step 1: Check if the warehouse is already stocked.
    # If we already have spots, we stop here so we don't create duplicates.
    if db.query(ParkingSpot).count() > 0:
        return

    spots_to_add = []

    # Step 2: Row A - 10 Regular spots (A1 to A10)
    for i in range(1, 11):
        spots_to_add.append(ParkingSpot(code=f"A{i}", spot_type=SpotType.REGULAR))

    # Step 3: Row B - 10 Regular spots (B1 to B10)
    for i in range(1, 11):
        spots_to_add.append(ParkingSpot(code=f"B{i}", spot_type=SpotType.REGULAR))

    # Step 4: Row C - 5 Disabled (C1-C5) and 5 Electric (C6-C10)
    for i in range(1, 6):
        spots_to_add.append(ParkingSpot(code=f"C{i}", spot_type=SpotType.DISABLED))

    for i in range(6, 11):
        spots_to_add.append(ParkingSpot(code=f"C{i}", spot_type=SpotType.ELECTRIC))

    # Step 5: Save all 30 spots to the database warehouse at once
    db.add_all(spots_to_add)
    db.commit()