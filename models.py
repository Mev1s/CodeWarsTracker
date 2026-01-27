from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username_telegram = Column(String, unique=True)
    telegram_id = Column(BigInteger, unique=True, nullable=True)

class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    followers = Column(Integer)
    allies = Column(Integer)
    leaders_board = Column(String)
    honor_percentile = Column(String)
    honor = Column(Integer)
    rank = Column(String)
    total_completed = Column(Integer)
    saved_at = Column(DateTime, server_default=func.now())
