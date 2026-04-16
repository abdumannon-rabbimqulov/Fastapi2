from sqlalchemy import select
from users.models import User
from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from users.schemas import SignUpSchema,LoginSchema
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from users.auth import hash_password
from users.crud import login_crud


router=APIRouter(prefix='/user',tags=['auth'])


@router.post("/sign-up")
async def sign_up(user:SignUpSchema,db:AsyncSession=Depends(get_db)):
    username=await db.execute(select(User).where(User.username==user.username))
    email=await db.execute(select(User).where(User.email==user.email))
    db_username=username.scalar_one_or_none()
    db_email=email.scalar_one_or_none()

    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='bu username band')
    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='bu email band')
    user=User(
        first_name=user.first_name,
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    response={
        'status':status.HTTP_201_CREATED,
        "message":"ro'yxatdan o'tdiz",
        "data":{
            "username":user.username,
            "email":user.email
        }
    }
    return response


@router.post("/login")
async def login(user:LoginSchema,db:AsyncSession=Depends(get_db)):
    return await login_crud(user,db)