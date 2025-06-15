from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from shemas import User_login,Token_Info
from models import UsersORM
from core import get_db_session,AsyncSession,check_pass,create_access_token,create_refresh_token,set_cookie

router = APIRouter()


async def valide_login(stored_user : User_login,session : AsyncSession = Depends(get_db_session)):
    query = (
        select(UsersORM)
        .filter(UsersORM.username == stored_user.username)
    )
    result = await session.execute(query)
    user = result.scalars().first()

    if not stored_user or not check_pass(stored_user.password,user.password):
        raise HTTPException(status_code=401,detail=("Incorrect username or password"))
    
    return user


@router.post("/login",response_model= Token_Info)
async def user_login(stored_user : User_login = Depends(valide_login)):

    access_token = create_access_token(stored_user)

    refresh_token = create_refresh_token(stored_user)

    response =  JSONResponse(content={"mesage":"Login  successful "})
    
    set_cookie(response,"access_token",access_token,60*15)
    set_cookie(response,"refresh_token",refresh_token,60*24*3600)
    

    return response