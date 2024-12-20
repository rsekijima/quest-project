import uuid

from sqlmodel import Field, SQLModel

class RewardBase(SQLModel):
    reward_name: str = Field(unique=True, index=True, max_length=255)
    reward_item: str | None = Field(default=None)
    reward_qty: int = Field(default=1)

class Reward(RewardBase, table=True):
    reward_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
class RewardCreate(RewardBase):
    reward_name: str = Field(max_length=255)
    reward_item: str = Field(min_length=1, max_length=255)
    reward_qty: int = 1

class QuestBase(SQLModel):
    auto_claim: bool = Field(default=False)
    streak: int = Field(default=0)
    duplication: int = Field(default=0)
    name: str = Field(unique=True, index=True, max_length=255)
    description: str | None = Field(default=None)

class Quest(QuestBase, table=True):
    quest_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    reward_id: uuid.UUID = Field(foreign_key="reward.reward_id")

class QuestCreate(QuestBase):
    pass
