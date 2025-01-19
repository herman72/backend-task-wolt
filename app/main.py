from fastapi import FastAPI
from app.routers.delivery import router as delivery_router

app = FastAPI(
    title="Delivery Order Price Calculator",
    description="API for calculating delivery order prices based on cart value, user location, and venue details.",
    version="1.0.0"
)

app.include_router(delivery_router, prefix="/api/v1", tags=["Delivery"])

@app.get("/")
def root():
    return {"message": "Welcome to the Delivery Order Price Calculator API!"}
