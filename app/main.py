from fastapi import FastAPI

# Initialize the FastAPI application
app = FastAPI(
    title="BloodShare API",
    description="Urgent Donation Network API",
    version="0.1.0",
)


@app.get("/hello_world")
def hello_world():
    """Endpoint returning welcome message."""
    return {"message": "Hello World from BloodShare"}


@app.get("/health")
def read_health():
    """Health check endpoint to verify the service status."""
    return {"status": "ok"}
