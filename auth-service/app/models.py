import uuid

from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

# Shared properties
class UserBase(SQLModel):
    user_name: str = Field(unique=True, index=True, max_length=255)
    status: int = 0
    gold: int = 0
    diamond: int = 0


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    user_name: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

class UserUpdate(UserBase):
    user_name: str | None = Field(default=None, index=True, max_length=255)
    status: int # type: ignore

# Properties to return via API, id is always required
class UserPublic(UserBase):
    user_id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None

class Event(BaseModel):
    event_type: str
    user_id: uuid.UUID
    timestamp: datetime