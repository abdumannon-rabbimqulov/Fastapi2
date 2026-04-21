from orders.schemas import CardItemCreate
from orders.models import Card,CardItem
from sqlalchemy.ext.asyncio import AsyncSession


async def add_item_to_card(card_id: int, item_data: CardItemCreate, db: AsyncSession):

    new_item = CardItem(**item_data.model_dump(), card_id=card_id)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item