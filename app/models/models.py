import enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base


# This satisfies the optional extra task: different types of parking spots
class SpotType(str, enum.Enum):
    REGULAR = "REGULAR"
    ELECTRIC = "ELECTRIC"
    DISABLED = "DISABLED"


class ParkingSpot(Base):
    __tablename__ = "parking_spots"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)  # e.g., "A1", "B2"
    spot_type = Column(Enum(SpotType), default=SpotType.REGULAR, nullable=False)
    is_active = Column(Boolean, default=True)

    # One-to-Many relationship with reservations
    reservations = relationship("Reservation", back_populates="spot", cascade="all, delete-orphan")


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    spot_id = Column(Integer, ForeignKey("parking_spots.id"), nullable=False)

    # "Kérelmező" (Applicant) from the assignment spec[cite: 1]
    license_plate = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    # Links back to the parking spot
    spot = relationship("ParkingSpot", back_populates="reservations")