from core import AsyncSession,get_db_session,decode_token,access_token
from models import UsersORM
from sqlalchemy import select
from fastapi import Depends,HTTPException,Request
import jwt

async def check_token(request : Request,session : AsyncSession = Depends(get_db_session)):
    token = request.cookies.get("access_token")
    if not token :
        raise HTTPException(status_code=401,detail="Authentication required")
    try:
        payload = decode_token(token)
        user_id = payload.get("user_id")
        email = payload.get("email")
        token_type = payload.get("token_type")
    
        if token_type != access_token:
           raise HTTPException(status_code=401,detail="Invalid token")
    
        if not user_id or not email:
           raise HTTPException(status_code=401, detail="Invalid token payload")
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Authentication required")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid token")
    
    query = (
        select(UsersORM)
        .filter(UsersORM.id == user_id,UsersORM.email == email)
    )
    result = await session.execute(query)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code= 401,detail = "User Not found")
    return user
