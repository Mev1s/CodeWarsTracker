from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from typing import Optional, List, Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


from database import engine, SessionLocal

app = FastAPI()



