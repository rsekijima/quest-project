import uuid

from sqlmodel import Field, SQLModel

from datetime import datetime

class UserQuestRewardBase(SQLModel):
    user_id: uuid.UUID 
    quest_id: uuid.UUID
    status: int = Field(default=0)
    streak: int = Field(default=0)
    duplication: int = Field(default=0)

class UserQuestReward(UserQuestRewardBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class EventBase(SQLModel):
    event_type: str
    user_id: uuid.UUID
    timestamp: datetime

class EventCreate(EventBase):
    event_type: str
    user_id: uuid.UUID
    timestamp: datetime

class Event(EventBase,table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
