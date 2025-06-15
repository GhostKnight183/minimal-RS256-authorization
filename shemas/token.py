from pydantic import BaseModel


class Token_Info(BaseModel):
    Token_type : str
    acces_token : str 
    refresh_token : str | None = None
