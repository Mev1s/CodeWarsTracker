from pydantic import BaseModel, Field
from typing import Optional, List, Annotated

class UserBase(BaseModel):
    username_telegram: Annotated[str, Field(..., title="Username", max_length=100, min_length=3)]
    name: Annotated[str, Field(title="HimanName", max_length=100, min_length=3)]
    telegram_id: Annotated[int, Field(..., title="TelegramID")]

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

class UserStatsBase(BaseModel):
    username_codewars: Annotated[str, Field(title="UsernameCodeWars")]
    followers: Annotated[int, Field(title="Followers")]
    allies: Annotated[int, Field(title="Allies")]
    leaders_board_position: Annotated[str, Field(title="Leaders_board_position")]
    honor_percentile: Annotated[str, Field(title="Honor_percentile")]
    honor: Annotated[int, Field(title="Honor")]
    rank: Annotated[str, Field(title="Rank", max_length=10)]
    total_completed: Annotated[int, Field(title="Total Completed")]
    language: Annotated[str, Field(title="LanguageProgramming")]
    saved_at: Annotated[str, Field(title="SavedAt_time")]

class UserStats(UserStatsBase):
    id: int

    class Config:
        orm_mode = True