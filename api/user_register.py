from sqlalchemy import select
from models import UsersORM
from shemas import User_register
from core import get_db_session,AsyncSession,hash_pass
from fastapi import APIRouter,Depends,HTTPException

router = APIRouter()

async def valide_registrattion(stored_user : User_register,session : AsyncSession = Depends(get_db_session)):
    query = (
        select(UsersORM)
        .filter((stored_user.username == UsersORM.username) | (stored_user.email == UsersORM.email))
    )
    result = await session.execute(query)
    user = result.scalars().first()
    if user:
        raise HTTPException(status_code= 400,detail="user alredy registed")
    
    return stored_user


@router.post("/registration")
async def user_register(user : User_register = Depends(valide_registrattion),session : AsyncSession = Depends(get_db_session)):
    hashed_pass = hash_pass(user.password)
    new_user = UsersORM(
        username = user.username,
        email = user.email,
        password = hashed_pass
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return "HI"