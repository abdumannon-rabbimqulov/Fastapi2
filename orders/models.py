from sqlalchemy import Column,Integer,Numeric,ForeignKey,Enum,DateTime
from db import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from products.models import Products


class Card(Base):
    __tablename__ = "cards"
    id =Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    items = relationship("CardItem", back_populates="card", cascade="all, delete-orphan")




class CardItem(Base):
    __tablename__ = "card_items"

    id = Column(Integer, primary_key=True)

    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    quantity = Column(Integer, default=1, nullable=False)


    card = relationship("Card", back_populates="items")
    product = relationship("Products")


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False
    )

    total_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Products")