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
    db_email=db.execute(select(User)).where(User.email==user.email)
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='bu username band')
    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='bu email band')
    user=User(**user.model_dump())

    await db.add(user)
    await db.commit()
    await db.refresh(user)


