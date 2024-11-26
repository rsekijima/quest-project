from typing import Any
import uuid

from fastapi import APIRouter

from app.models import Reward
from app.api.deps import (
    SessionDep
)
from app.crud import get_reward_by_id

router = APIRouter()


@router.get("/{reward_id}", response_model=Reward)
def read_reward_by_id(
    reward_id: uuid.UUID, session: SessionDep
) -> Any:
    """
    Get a specific reward by id.
    """
    reward = get_reward_by_id(session=session, reward_id=reward_id)
    return reward