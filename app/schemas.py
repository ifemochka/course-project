from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, constr


class SuggestionCreate(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=200)
    text: constr(strip_whitespace=True, max_length=1000) = ""
    user_id: constr(strip_whitespace=True, min_length=1, max_length=50)


class SuggestionUpdate(BaseModel):
    title: Optional[constr(strip_whitespace=True, min_length=1, max_length=200)] = None
    text: Optional[constr(strip_whitespace=True, max_length=1000)] = None
    status: Optional[str] = None


class ProblemDetailException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_type: str = "about:blank"):
        super().__init__(status_code=status_code, detail=detail)
        self.error_type = error_type
