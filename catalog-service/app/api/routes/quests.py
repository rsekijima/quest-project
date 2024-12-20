from typing import Any
import uuid

from fastapi import APIRouter

from app.models import Quest
from app.api.deps import (
    SessionDep
)
from app.crud import get_quest_by_name, get_quest_by_id

router = APIRouter()

@router.get("/{quest_id}", response_model=Quest)
def read_quest_by_id(
    quest_id: uuid.UUID, session: SessionDep
) -> Any:
    """
    Get a specific quest by id.
    """
    quest = get_quest_by_id(session=session, quest_id=quest_id)
    return quest


@router.get("/name/{quest_name}", response_model=Quest)
def read_quest_by_name(
    quest_name: str, session: SessionDep
) -> Any:
    """
    Get a specific quest by name.
    """
    quest = get_quest_by_name(session=session, name=quest_name)
    return quest