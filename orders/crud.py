from sqlalchemy import select
from sqlalchemy.orm import selectinload
from orders.schemas import CardItemCreate
from orders.models import Card,CardItem
from sqlalchemy.ext.asyncio import AsyncSession


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
