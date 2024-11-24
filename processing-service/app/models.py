import uuid

from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Column
from typing import Dict, Any
from sqlalchemy.dialects.postgresql import JSON

from datetime import datetime

class UserQuestRewardBase(SQLModel):
    user_id: uuid.UUID 
    quest_id: uuid.UUID
    status: int = Field(default=0)
    streak: int = Field(default=0)
    duplication: int = Field(default=0)

class UserQuestRewardCreate(UserQuestRewardBase):
    pass

class UserQuestRewardUpdate(UserQuestRewardBase):
    user_id: uuid.UUID | None = Field(default=None)
    quest_id: uuid.UUID | None = Field(default=None)
    status: int | None = Field(default=None)
    streak: int | None = Field(default=None)
    duplication: int | None = Field(default=None)


class UserQuestReward(UserQuestRewardBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class EventBase(SQLModel):
    event_type: str
    user_id: uuid.UUID
    timestamp: datetime
    event_data: Dict[str, Any] = Field(
        default={},
        sa_column=Column(JSON)
    )

class EventCreate(EventBase):
    pass

class EventPublish(EventBase):
    pass

class Event(EventBase,table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class Quest(BaseModel):
    auto_claim: bool 
    streak: int 
    duplication: int 
    name: str
    description: str | None 
    quest_id: uuid.UUID
    reward_id: uuid.UUID