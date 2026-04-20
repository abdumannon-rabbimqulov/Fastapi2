from sqlalchemy import Column,Integer,Numeric,ForeignKey
from db import Base
from sqlalchemy.orm import relationship


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
    product = relationship("Product")