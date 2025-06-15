from pydantic import BaseModel,EmailStr
from typing import Annotated

class User_register(BaseModel):
    email : Annotated[str,EmailStr]
    username : str
    password : str

class User_login(BaseModel):
    username:str
    password:str