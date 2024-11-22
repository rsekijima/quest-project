import jwt
from fastapi import APIRouter, HTTPException
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.core.config import settings
from app.models import TokenPayload
from app.core import security

router = APIRouter()

@router.post("/validate-token")
def validate_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        return payload
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

@router.get("/health-check/")
async def health_check() -> bool:
    return True
