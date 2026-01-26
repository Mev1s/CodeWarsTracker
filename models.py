from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    name = Column(String)
    telegram_id = Column(Integer, unique=True, nullable=True)

class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    followers = Column(Integer)
    allies = Column(Integer)
    leaders_board = Column(Integer)
    Honor_percentile = Column(String)
    honor = Column(Integer)
    rank = Column(String)
    total_completed = Column(Integer)
    language = Column(String)
    saved_at = Column(DateTime, server_default=func.now())
