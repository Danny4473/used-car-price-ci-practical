
import logging
import sys
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)

logger = logging.getLogger("used-car-price-api")

app = FastAPI(
    title="Used Car Price Practical API",
    description="A simple API demo for the CI/CD practical",
    version="1.1.0",
)


class PriceRequest(BaseModel):
    quantity: int
    price_per_car: float


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    start_time = time.perf_counter()

    try:
        response = await call_next(request)
        duration = round((time.perf_counter() - start_time) * 1000, 2)
        response.headers["X-Request-ID"] = request_id

        logger.info(
            "event=request_completed request_id=%s method=%s path=%s status=%s duration_ms=%s",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        duration = round((time.perf_counter() - start_time) * 1000, 2)
        logger.exception(
            "event=request_failed request_id=%s method=%s path=%s duration_ms=%s",
            request_id,
            request.method,
            request.url.path,
            duration,
        )
        raise


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    logger.warning(
        "event=validation_error method=%s path=%s error_count=%s",
        request.method,
        request.url.path,
        len(exc.errors()),
    )

    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.on_event("startup")
async def log_startup():
    logger.info("event=application_started")


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
        logger.warning("event=invalid_quantity quantity=%s", request.quantity)
        return {"error": "Quantity must be positive"}

    if request.price_per_car < 0:
        logger.warning("event=invalid_price price_per_car=%s", request.price_per_car)
        return {"error": "Price cannot be negative"}

    total = round(request.quantity * request.price_per_car, 2)

    logger.info("event=calculation_success")

    return {
        "quantity": request.quantity,
        "price_per_car": request.price_per_car,
        "total": total,
    }
