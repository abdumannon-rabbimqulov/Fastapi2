from pydantic import BaseModel,Field
from typing import Optional



class SignUp(BaseModel):
    first_name :Optional[str]
    username :str=Field()