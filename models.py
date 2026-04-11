from db import Base
from sqlalchemy import Integer,Column,String


class Product(Base):
    __tablename__ = 'product'
    id =Column(Integer,primary_key=True)
    title=Column(String(100))
    desc=Column(String)