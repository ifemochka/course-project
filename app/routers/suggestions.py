from enum import Enum
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/suggestions", tags=["suggestions"])

suggestions_db = []
current_id = 1


class SuggestionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@router.post("/")
def create_suggestion(title: str, text: str, user_id: str = Query(...)):
    global current_id
    suggestion = {
        "id": current_id,
        "title": title,
        "text": text,
        "user_id": user_id,
        "status": SuggestionStatus.PENDING
    }
    suggestions_db.append(suggestion)
    current_id += 1
    return suggestion


@router.get("/")
def get_suggestions(status: Optional[SuggestionStatus] = Query(None)):
    if status:
        return [s for s in suggestions_db if s["status"] == status]
    return suggestions_db


@router.get("/{suggestion_id}")
def get_suggestion(suggestion_id: int):
    for suggestion in suggestions_db:
        if suggestion["id"] == suggestion_id:
            return suggestion
    raise HTTPException(status_code=404, detail="Suggestion not found")


@router.put("/{suggestion_id}")
def update_suggestion(
    suggestion_id: int,
    title: str = None,
    text: str = None,
    status: SuggestionStatus = None
):
    for suggestion in suggestions_db:
        if suggestion["id"] == suggestion_id:
            if title is not None:
                suggestion["title"] = title
            if text is not None:
                suggestion["text"] = text
            if status is not None:
                suggestion["status"] = status
            return suggestion
    raise HTTPException(status_code=404, detail="Suggestion not found")


@router.delete("/{suggestion_id}")
def delete_suggestion(suggestion_id: int):
    global suggestions_db
    for i, suggestion in enumerate(suggestions_db):
        if suggestion["id"] == suggestion_id:
            del suggestions_db[i]
            return {"message": "Suggestion deleted"}
    raise HTTPException(status_code=404, detail="Suggestion not found")
