from pydantic import BaseModel
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