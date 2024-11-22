from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError
from app.models import TokenPayload
from app.core import security
from app.core.config import settings
from app.core.db import engine
from sqlmodel import Session

# Assuming reusable_oauth2 is already defined as in your code
router = APIRouter()

# You can reuse your existing method to validate the token and return the decoded payload
def validate_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        return TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

class TokenValidationResponse(BaseModel):
    valid: bool
    message: str

@router.post("/validate-token", response_model=TokenValidationResponse)
def validate_token_route(token: str = Depends(reusable_oauth2)):
    try:
        # Try to validate the token
        payload = validate_token(token)
        return TokenValidationResponse(valid=True, message="Token is valid",)
    except HTTPException:
        return TokenValidationResponse(valid=False, message="Token is invalid")
