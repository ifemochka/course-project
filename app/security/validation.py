import re

from fastapi import HTTPException


def validate_suggestion_data(title: str, text: str, user_id: str):
    """Валидация данных предложения"""

    if len(title) > 200:
        raise HTTPException(
            status_code=422,
            detail="Title exceeds maximum length of 200 characters"
        )

    if len(text) > 5000:
        raise HTTPException(
            status_code=422,
            detail="Text exceeds maximum length of 5000 characters"
        )

    if not re.match(r'^[a-zA-Z0-9\-_]+$', user_id):
        raise HTTPException(
            status_code=422,
            detail="Invalid user_id format"
        )

    return True
