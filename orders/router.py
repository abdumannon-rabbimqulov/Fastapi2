from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from orders.schemas import CardItemCreate, CardResponse,OrderResponse
from orders.crud import (
    add_item_to_card,delete,delete_card_all,
    order_create
)
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


@router.delete("/delete-card",response_model=None)
async def card_delete(
        pk:int,
        db:AsyncSession=Depends(get_db),
        user_id:int=Depends(get_current_user)
        ):

    db_product=await delete(
        pk=pk,
        db=db,
        user_id=user_id
    )

    if db_product in None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="product topilmadi")

    return HTTPException(status_code=status.HTTP_200_OK,detail="ochirildi")


@router.delete("/delete-card-all",response_model=None)
async def card_all_delete(
        db:AsyncSession=Depends(get_db),
        user_id:int=Depends(get_current_user)
        ):

    db_card=await delete_card_all(user_id=user_id,db=db)

    if not db_card:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="card topilmadi")

    return HTTPException(status_code=status.HTTP_200_OK,detail="o'chirildi")



@router.post("/order-create",response_model=OrderResponse)
async def create_order(user_id:int=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    db_order=await order_create(user_id=user_id,db=db)

    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Buyurtma yaratishda xatolik (savatcha bo'sh bo'lishi mumkin)"
        )

    return db_order


