import os
import time
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("bloodshare.database")

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://bloodshare_user:bloodshare_pass@localhost:5433/bloodshare_db",
)


def create_db_engine(url: str):
    """Creates SQLAlchemy engine with retry logic for container initialization."""
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}

    if not url.startswith("postgresql"):
        return create_engine(url, connect_args=connect_args)

    # Retry connection up to 5 times (useful while PostgreSQL container initializes)
    last_err = None
    for attempt in range(1, 6):
        try:
            eng = create_engine(url, pool_pre_ping=True)
            with eng.connect():
                pass
            print(f"[BloodShare] Connected successfully to PostgreSQL at {url.split('@')[-1]}")
            return eng
        except Exception as exc:
            last_err = exc
            print(f"[BloodShare] PostgreSQL connection attempt {attempt}/5 failed ({exc}). Retrying in 2s...")
            time.sleep(2)

    fallback_url = "sqlite:///./bloodshare.db"
    print(f"[BloodShare] Warning: Could not reach PostgreSQL ({last_err}). Falling back to SQLite ({fallback_url})")
    return create_engine(fallback_url, connect_args={"check_same_thread": False})


engine = create_db_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Yield a database session and ensure it closes after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
