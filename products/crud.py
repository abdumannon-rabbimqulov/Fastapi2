from fastapi import status
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from products.schemas import ProductBase,ProductCreate,ProductResponse,ProductUpdate
from products.models import Products
from sqlalchemy.ext.asyncio import AsyncSession



async def create_product(data:ProductCreate,db:AsyncSession):
    product=Products(**data.model_dump())

    try:
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product
    except Exception as e:
        await db.rollback()
        raise e


async def update_product(pk:int,data:ProductUpdate,db:AsyncSession):
    result=await db.execute(select(Products)).where(Products.id==pk)
    product=result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="product topilmadi ")

    update_data=data.model_dump(exclude_unset=True)

    for key,value in update_data.items():

        setattr(product,key,value)

    await db.commit()
    await db.refresh(product)
    return product

async def get_all(db:AsyncSession):
    result=await db.execute(select(Products))
    products=result.scalars().all()
    return products


async def get(product_id: int, db: AsyncSession):
    result = await db.execute(select(Products).where(Products.id == product_id))
    product = result.scalar_one_or_none()
    return product


async def delete(product_id: int, db: AsyncSession):
    result = await db.execute(select(Products).where(Products.id == product_id))
    db_product = result.scalar_one_or_none()
    if not db_product:
        return None

    await db.delete(db_product)
    await db.commit()
    return True