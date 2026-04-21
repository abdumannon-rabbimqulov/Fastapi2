from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from products.schemas import ProductResponse

class CardItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CardItemUpdate(BaseModel):
    quantity: int

class CardItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductResponse
    model_config = ConfigDict(from_attributes=True)


class CardCreate(BaseModel):
    user_id: int

class CardResponse(BaseModel):
    id: int
    user_id: int
    items: List[CardItemResponse] = []

    model_config = ConfigDict(from_attributes=True)