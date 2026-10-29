import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables from .env file
load_dotenv()

# Read database connection string from environment with a fallback default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/bloodshare",
)

# SQLAlchemy engine - connection is created lazily, so server starts without an active DB
engine = create_engine(DATABASE_URL)

# Factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy declarative models
Base = declarative_base()


# Dependency to obtain a database session in FastAPI routers
def get_db():
    """Yield a database session and ensure it closes after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
