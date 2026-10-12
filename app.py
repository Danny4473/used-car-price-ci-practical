
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Used Car Price Practical API",
    description="A simple API demo for the CI/CD practical",
    version="1.0.0",
)


class PriceRequest(BaseModel):
    quantity: int
    price_per_car: float


@app.get("/")
def home():
    return {
        "message": "Used Car Price API is running!",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/calculate-total")
def calculate_total(request: PriceRequest):
    if request.quantity <= 0:
        return {"error": "Quantity must be positive"}

    if request.price_per_car < 0:
        return {"error": "Price cannot be negative"}

    return {
        "quantity": request.quantity,
        "price_per_car": request.price_per_car,
        "total": round(request.quantity * request.price_per_car, 2),
    }
