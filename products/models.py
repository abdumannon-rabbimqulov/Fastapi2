from db import Base
from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime,ForeignKey
from sqlalchemy.sql import func


class Products(Base):
    __tablename__ = "products"
    id =Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    title = Column(String(100))
    price=Column(Numeric(10,2),nullable=False)
    desc=Column(Text)
    created_at=Column(DateTime(timezone=True), server_default=func.now())