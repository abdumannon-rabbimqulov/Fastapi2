from sqlalchemy.ext.asyncio import AsyncSession
from Schems import ProductCreate
from models import Product


async def Create(db:AsyncSession,data:ProductCreate):
    product=Product(**data.model_dump())
    await  db.add(product)
    await  db.commit()
    await  db.refresh(product)
    return product

