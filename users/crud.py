from users.schemas import LoginSchema
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import User
from sqlalchemy import select
from fastapi import status
from fastapi.exceptions import HTTPException
from users.auth import verify_password,create_access_token,create_refresh_token


async def login_crud(data:LoginSchema,db:AsyncSession):
    result=await db.execute(select(User).where(User.username==data.username))
    db_user=result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="username topilmadi")

    is_valid=verify_password(data.password,db_user.password)

    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="parol xato")

    token_data={"sub":str(db_user.id)}

    refresh_token=create_refresh_token(token_data)
    access_token=create_access_token(token_data)

    response={
        "status":status.HTTP_200_OK,
        "message":"login qilindi",
        "refresh":refresh_token,
        "access":access_token
    }

    return response

