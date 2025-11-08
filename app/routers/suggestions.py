from enum import Enum
from typing import Optional

from fastapi import APIRouter, Query

from app.schemas import ProblemDetailException, SuggestionCreate, SuggestionUpdate

router = APIRouter(prefix="/suggestions", tags=["suggestions"])

suggestions_db = []
current_id = 1


class SuggestionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@router.post("/")
def create_suggestion(suggestion: SuggestionCreate):
    global current_id
    suggestion_data = {
        "id": current_id,
        "title": suggestion.title,
        "text": suggestion.text,
        "user_id": suggestion.user_id,
        "status": SuggestionStatus.PENDING.value,
    }
    suggestions_db.append(suggestion_data)
    current_id += 1
    return suggestion_data


@router.get("/")
def get_suggestions(status: Optional[SuggestionStatus] = Query(None)):
    if status:
        return [s for s in suggestions_db if s["status"] == status.value]
    return suggestions_db


@router.get("/{suggestion_id}")
def get_suggestion(suggestion_id: int):
    for suggestion in suggestions_db:
        if suggestion["id"] == suggestion_id:
            return suggestion
    raise ProblemDetailException(
        status_code=404,
        detail="Suggestion not found",
        error_type="https://example.com/not-found",
    )


@router.put("/{suggestion_id}")
def update_suggestion(suggestion_id: int, update_data: SuggestionUpdate):
    for suggestion in suggestions_db:
        if suggestion["id"] == suggestion_id:
            update_dict = update_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                if value is not None:
                    suggestion[field] = value
            return suggestion
    raise ProblemDetailException(
        status_code=404,
        detail="Suggestion not found",
        error_type="https://example.com/not-found",
    )


@router.delete("/{suggestion_id}")
def delete_suggestion(suggestion_id: int):
    global suggestions_db
    for i, suggestion in enumerate(suggestions_db):
        if suggestion["id"] == suggestion_id:
            del suggestions_db[i]
            return {"message": "Suggestion deleted"}
    raise ProblemDetailException(
        status_code=404,
        detail="Suggestion not found",
        error_type="https://example.com/not-found",
    )
