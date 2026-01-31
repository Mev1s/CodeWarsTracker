from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from typing import Optional, List, Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database import engine, SessionLocal, db_add
from schemas import User as UsersScheme, UserStats as UserStatsScheme, UserCreate
from models import User as UserModel, UserStats as UserStatsModel

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/users", response_model=List[UsersScheme])
def get_users(db: Session = Depends(get_db)) -> List[UsersScheme]:
    users = db.query(UserModel).all()
    return users

@app.get("/user_stats", response_model=List[UserStatsScheme])
def get_user_stats(db: Session = Depends(get_db)) -> List[UserStatsScheme]:
    user_stats = db.query(UserStatsModel).all()
    return user_stats

@app.post("/users", response_model=UsersScheme)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UsersScheme:
    new_user = UserModel(username_codewars=user.username_codewars, username_telegram=user.username_telegram, telegram_id=user.telegram_id)
    db_add(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=UsersScheme)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UsersScheme:
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user







