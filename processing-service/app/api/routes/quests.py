from typing import Any
import uuid

from fastapi import APIRouter

from app.models import Quest
from app.api.deps import (
    SessionDep
)

router = APIRouter()


@router.get("/{quest_id}", response_model=Quest)
def read_quest_by_id(
    quest_id: uuid.UUID, session: SessionDep
) -> Any:
    """
    Get a specific quest by id.
    """
    return session.get(Quest, quest_id)