from typing import List

from  fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from users.auth import get_current_user
from Post.schemas import *
from db import get_db
from Post.crud import create_product,get,get_all,update_product,delete
from fastapi.exceptions import HTTPException


router=APIRouter(prefix="/product",tags=["Post"])




@router.post("/create", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_new_product(
        data: ProductCreate,
        db: AsyncSession = Depends(get_db),
        user_id:int=Depends(get_current_user)):

    new_product= await create_product(db=db, data=data,user_id=user_id)
    if not new_product:
        raise HTTPException(status_code=400, detail="Mahsulot yaratishda xatolik!")

    return new_product


@router.get("/", response_model=List[ProductResponse])
async def get_products(
        db: AsyncSession = Depends(get_db),
        user_id:int=Depends(get_current_user)):
    products=await get_all(
        db=db,
        user_id=user_id
    )

    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_one(product_id: int,
                      db: AsyncSession = Depends(get_db),
                      user_id:int=Depends(get_current_user)):
    product = await get(
        product_id=product_id,
        db=db,
        user_id=user_id
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product





@router.put("/{product_id}", response_model=ProductResponse)
async def update(
        pk: int,
        product_update: ProductUpdate,
        db: AsyncSession = Depends(get_db),
        user_id:int=Depends(get_current_user)
):
    db_product = await update_product(
        db=db,
        pk=pk,
        data=product_update,
        user_id=user_id
    )


    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product_id: int,
        db: AsyncSession = Depends(get_db),
        user_id:int=Depends(get_current_user)
        ):
    db_product =await delete(
        product_id=product_id,
        db=db,
        user_id=user_id
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
