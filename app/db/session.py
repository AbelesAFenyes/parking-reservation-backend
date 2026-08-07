import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# If Docker hands us a PostgreSQL URL, use it. Otherwise, fallback to our local SQLite file.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./parking.db")

# SQLite needs 'check_same_thread', PostgreSQL does not!
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()