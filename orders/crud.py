from sqlalchemy import select
from fastapi.exceptions import HTTPException
from fastapi import status
from orders.schemas import CardItemCreate,OrderCreate
from orders.models import Card, CardItem, OrderItem
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from orders.models import Order


async def add_item_to_card(user_id: int, item_data: CardItemCreate, db: AsyncSession):
    result=await db.execute(select(Card).where(Card.user_id==user_id))
    card=result.scalar_one_or_none()

    if not card:
        card=Card(user_id=user_id)
        db.add(card)
        await db.flush()

    item_result = await db.execute(
        select(CardItem).where(
            CardItem.card_id == card.id,
            CardItem.product_id == item_data.product_id
        )
    )
    existing_item = item_result.scalar_one_or_none()

    if existing_item:
        existing_item.quantity += item_data.quantity

        if existing_item.quantity <= 0:
            await db.delete(existing_item)
            return None
    else:
        if item_data.quantity > 0:
            new_item = CardItem(
                card_id=card.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity
            )
            db.add(new_item)

    await db.commit()
    await db.refresh(card)
    return card


async def delete(user_id:int,pk:int,db:AsyncSession):
    result=await db.execute(select(CardItem).where(
        CardItem.product_id==pk,
        CardItem.card.user_id==user_id
    ))

    db_product=result.scalar_one_or_none()

    if not db_product:
        return None

    await db.delete(db_product)
    await db.commit()
    return True


async def delete_card_all(user_id:int,db:AsyncSession):
    result=await db.execute(select(Card).where(Card.user_id==user_id))
    db_card=result.scalar_one_or_none()

    if db_card:

        await db.delete(db_card)
        await db.commit()
        return True
    return False


async def order_create(user_id:int,db:AsyncSession):
    result =await db.execute(select(Card).where(Card.user_id==user_id))
    card=result.scalar_one_or_none()

    if not card:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Savatcha topilmadi")

    result=await db.execute(select(CardItem).where(CardItem.card_id==card.id))
    cart_items=result.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Savatcha bo'sh")


    try:
        total_price=Decimal("0.0")
        order_items_to_create=[]


        new_order=Order(
            user_id=user_id,
            total_price=0
        )
        db.add(new_order)
        await db.flush()


        for item in cart_items:

            current_price=item.product.price

            item_total=current_price*item.quantity

            total_price+=item_total

            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=current_price
            )
            order_items_to_create.append(order_item)

        new_order.total_price=total_price
        db.add_all(order_items_to_create)

        for item in cart_items:
            await db.delete(item)

        await db.commit()
        await db.refresh(new_order)
        return new_order


    except Exception as e:
        await db.rollback()
        raise e


