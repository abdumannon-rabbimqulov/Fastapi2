from sqlalchemy import select

from users.models import User
from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from users.schemas import SignUpSchema
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db


router=APIRouter(prefix='/user',tags=['auth'])


@router.post("/sign-up")
async def sign_up(user:SignUpSchema,db:AsyncSession=Depends(get_db)):
    db_username=db.execute(select(User)).where(User.username==user.username)

    
