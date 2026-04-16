from pydantic import BaseModel,Field
from typing import Optional



class SignUpSchema(BaseModel):
    first_name :Optional[str]
    username :str
    email :str
    password :str
