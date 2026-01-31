from pydantic import BaseModel, Field
from typing import Optional, List, Annotated, Union
from datetime import datetime


class UserBase(BaseModel):
    username_codewars: Annotated[Optional[str], Field(title="UsernameCodeWars")] = None
    username_telegram: Annotated[str, Field(..., title="Username", max_length=100, min_length=3)]
    telegram_id: Annotated[int, Field(..., title="TelegramID")]

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass

class UserStatsBase(BaseModel):
    user_id: Annotated[int, Field(title="UserID = users.id")]
    followers: Annotated[int, Field(title="Followers")]
    allies: Annotated[int, Field(title="Allies")]
    leaders_board: Annotated[str, Field(title="Leaders_board_position")]
    honor_percentile: Annotated[str, Field(title="Honor_percentile")]
    honor: Annotated[int, Field(title="Honor")]
    rank: Annotated[str, Field(title="Rank", max_length=10)]
    total_completed: Annotated[int, Field(title="Total Completed")]
    saved_at: datetime

class UserStats(UserStatsBase):
    id: int

    class Config:
        from_attributes = True