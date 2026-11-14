import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from http import HTTPStatus

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import Base, SessionLocal, engine
from app.routers import alerts_router, donors_router, inventory_router, zones_router
from app.seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes tables and seeds initial development data on startup."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="BloodShare – Urgent Donation Network API",
    description="RESTful API tracking blood shortages and alerting matching donors.",
    version="0.1.0",
    lifespan=lifespan,
)


def _format_timestamp() -> str:
    """Returns current UTC timestamp in ISO 8601 format with trailing Z."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom exception handler conforming to README standard error schema."""
    first_error = exc.errors()[0] if exc.errors() else {}
    error_msg = first_error.get("msg", "Invalid request payload.")

    # Remove Pydantic's default prefix "Value error, " if present
    if error_msg.startswith("Value error, "):
        error_msg = error_msg.replace("Value error, ", "")

    # Clean up missing field messages
    loc = first_error.get("loc", [])
    if first_error.get("type") == "missing" and loc:
        field_name = loc[-1]
        error_msg = f"Field '{field_name}' is required."

    payload = {
        "status": status.HTTP_400_BAD_REQUEST,
        "error": "Bad Request",
        "message": error_msg,
        "timestamp": _format_timestamp(),
    }
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=payload)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Custom HTTP exception handler conforming to README standard error schema."""
    try:
        error_title = HTTPStatus(exc.status_code).phrase
    except ValueError:
        error_title = "Error"

    payload = {
        "status": exc.status_code,
        "error": error_title,
        "message": str(exc.detail),
        "timestamp": _format_timestamp(),
    }
    return JSONResponse(status_code=exc.status_code, content=payload)


# Include Feature Routers
app.include_router(zones_router)
app.include_router(donors_router)
app.include_router(inventory_router)
app.include_router(alerts_router)


# Utility Endpoints
@app.get("/hello_world", tags=["Utility"])
def hello_world():
    """Endpoint returning welcome message."""
    return {"message": "Hello World from BloodShare"}


@app.get("/health", tags=["Utility"])
def read_health():
    """Health check endpoint to verify the service status."""
    return {"status": "ok"}
