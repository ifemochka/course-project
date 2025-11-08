import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers import suggestions
from app.schemas import ProblemDetailException

app = FastAPI(title="SecDev Course App", version="0.1.0")


@app.exception_handler(ProblemDetailException)
async def problem_detail_handler(request: Request, exc: ProblemDetailException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": exc.error_type,
            "title": exc.detail,
            "status": exc.status_code,
            "instance": str(request.url),
            "correlation_id": str(uuid.uuid4()),
        },
        headers={"Content-Type": "application/problem+json"},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "loc": error["loc"],
                "msg": error["msg"],
                "type": error["type"],
            }
        )
    return JSONResponse(
        status_code=422,
        content={
            "type": "https://example.com/validation-error",
            "title": "Request validation failed",
            "status": 422,
            "instance": str(request.url),
            "correlation_id": str(uuid.uuid4()),
            "errors": errors,
        },
        headers={"Content-Type": "application/problem+json"},
    )


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(suggestions.router)
