from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from products.schemas import ProductResponse
from decimal import Decimal
from enum import Enum
from datetime import datetime


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



class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: Decimal
    product: Optional[ProductResponse] = None

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    total_price: Decimal

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total_price: Decimal
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

class OrderUpdateStatus(BaseModel):
    status: OrderStatus