from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db  # DB session funksiyangiz
from orders.schemas import CardItemCreate, CardResponse
from orders.crud import add_item_to_card
from users.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/add-cart", response_model=None)
async def add_to_cart(
        item_data: CardItemCreate,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await add_item_to_card(user_id=user_id, item_data=item_data, db=db)

    return {"message": "Mahsulot savatchaga muvaffaqiyatli qo'shildi"}