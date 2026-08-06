from pydantic import BaseModel
from datetime import datetime
from app.models.models import SpotType

# This defines exactly what the JSON response will look like
class ParkingSpotResponse(BaseModel):
    id: int
    code: str
    spot_type: SpotType
    is_active: bool

    class Config:
        # This tells Pydantic to read directly from our SQLAlchemy database models
        from_attributes = True

# What the user sends us to create a booking
class ReservationCreate(BaseModel):
    spot_id: int
    license_plate: str
    start_time: datetime
    end_time: datetime
    is_electric_vehicle: bool = False
    has_disabled_permit: bool = False

# What we send back to the user after a successful booking
class ReservationResponse(BaseModel):
    id: int
    spot_id: int
    license_plate: str
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True