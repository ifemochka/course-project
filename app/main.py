from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, constr
from typing import Optional
import uuid

from app.routers import suggestions

app = FastAPI(title="SecDev Course App", version="0.1.0")


# Контроль 1: Валидация ввода
class SuggestionCreate(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=200)
    text: constr(strip_whitespace=True, max_length=1000) = ""
    user_id: constr(strip_whitespace=True, min_length=1, max_length=50)


class SuggestionUpdate(BaseModel):
    title: Optional[constr(strip_whitespace=True, min_length=1, max_length=200)] = None
    text: Optional[constr(strip_whitespace=True, max_length=1000)] = None
    status: Optional[str] = None


# Контроль 2: RFC 7807 ошибки
class ProblemDetailException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_type: str = "about:blank"):
        super().__init__(status_code=status_code, detail=detail)
        self.error_type = error_type


@app.exception_handler(ProblemDetailException)
async def problem_detail_handler(request: Request, exc: ProblemDetailException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": exc.error_type,
            "title": exc.detail,
            "status": exc.status_code,
            "instance": str(request.url),
            "correlation_id": str(uuid.uuid4())
        },
        headers={"Content-Type": "application/problem+json"}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "type": "https://example.com/validation-error",
            "title": "Request validation failed",
            "status": 422,
            "instance": str(request.url),
            "correlation_id": str(uuid.uuid4()),
            "errors": errors
        },
        headers={"Content-Type": "application/problem+json"}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, str) else "http_error"
    raise ProblemDetailException(
        status_code=exc.status_code,
        detail=detail,
        error_type=f"https://example.com/http-error-{exc.status_code}"
    )


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(suggestions.router)