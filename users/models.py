from sqlalchemy import Integer,String,BigInteger,Boolean,Column,DateTime
from db import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    first_name=Column(String(50),nullable=True)
    username=Column(String(50),unique=True)
    email=Column(String(50),unique=True)
    password=Column(String())

    is_staff=Column(Boolean,default=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now())
    updated_at=Column(DateTime,default=datetime.now())


    def __repr__(self):
        return self.username

