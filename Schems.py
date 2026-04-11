from pydantic import BaseModel

class ProductBase(BaseModel):
    id : int
    title: str
    desc: str

class ProductCreate(ProductBase):
    pass

class ProductGet(ProductBase):
    pass


class ProductResponse(ProductBase):
    id:int
    title: str
