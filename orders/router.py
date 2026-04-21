from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from orders.schemas import CardItemCreate, CardResponse
from orders.crud import add_item_to_card
from users.auth import get_current_user
from fastapi.exceptions import HTTPException
from fastapi import status

router = APIRouter(prefix="/order", tags=["Cart"])


@router.post("/add-cart", response_model=None)
async def add_to_cart(
        item_data: CardItemCreate,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await add_item_to_card(user_id=user_id, item_data=item_data, db=db)

    if result is None:
        raise HTTPException(detail="ochirildi",status_code=status.HTTP_200_OK)

    return {"message": "Mahsulot savatchaga muvaffaqiyatli qo'shildi"}



