from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey
import datetime
from .base import Base
from typing import Annotated

fcx = Annotated[int,mapped_column(primary_key=True)]


class UsersORM(Base):
    __tablename__ = "Users"
    id : Mapped[fcx]
    username : Mapped[str] = mapped_column(unique= True)
    password : Mapped[bytes] 
    email : Mapped[str] = mapped_column(unique=True)
    created_at : Mapped[datetime.datetime] = mapped_column(default= datetime.datetime.utcnow())
    is_admin: Mapped[bool] = mapped_column(default=False)

