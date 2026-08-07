import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import Base, get_db
from app.db.seed import seed_data
from app.models.models import SpotType

# 1. Create a completely separate, temporary database just for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_parking.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Build the temporary database
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
test_db = TestingSessionLocal()
seed_data(test_db)
test_db.close()

# 3. Swap out the real database for the fake one
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 4. Give ourselves a robotic web browser to click the buttons
client = TestClient(app)

# --- THE ACTUAL TESTS ---

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Parking API is running!"}

def test_get_all_spots():
    # Because we haven't run the seed script on this test database, it should be empty initially
    response = client.get("/api/v1/spots")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_invalid_time_reservation():
    # Trying to book an end time that happens before the start time
    response = client.post(
        "/api/v1/reservations",
        json={
            "spot_id": 1,
            "license_plate": "TEST-123",
            "start_time": "2026-10-10T12:00:00",
            "end_time": "2026-10-10T10:00:00",
            "is_electric_vehicle": False,
            "has_disabled_permit": False
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "The end time must be after the start time."


def test_create_overlap_reservation():
    # 1. We create a valid booking from 10:00 to 12:00
    client.post(
        "/api/v1/reservations",
        json={
            "spot_id": 1,
            "license_plate": "VALID-1",
            "start_time": "2026-10-10T10:00:00",
            "end_time": "2026-10-10T12:00:00",
            "is_electric_vehicle": False,
            "has_disabled_permit": False
        }
    )

    # 2. We try to book the exact same spot from 11:00 to 13:00 (this overlaps!)
    response = client.post(
        "/api/v1/reservations",
        json={
            "spot_id": 1,
            "license_plate": "OVERLAP-2",
            "start_time": "2026-10-10T11:00:00",
            "end_time": "2026-10-10T13:00:00",
            "is_electric_vehicle": False,
            "has_disabled_permit": False
        }
    )

    # 3. We assert that the bouncer kicks us out with a 409 Conflict
    assert response.status_code == 409
    assert response.json()["detail"] == "This parking spot is already booked for the requested time."


def test_create_reservation_wrong_vehicle_type():
    # We try to book spot ID 26 (which is C6, an electric spot in our database)
    response = client.post(
        "/api/v1/reservations",
        json={
            "spot_id": 26,
            "license_plate": "GAS-CAR",
            "start_time": "2026-10-11T10:00:00",
            "end_time": "2026-10-11T12:00:00",
            "is_electric_vehicle": False,  # Missing the requirement!
            "has_disabled_permit": False
        }
    )

    # We assert that the bouncer blocks a non-electric car with a 400 Bad Request
    assert response.status_code == 400
    assert response.json()["detail"] == "This spot is reserved for electric vehicles only."