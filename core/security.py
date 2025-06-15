from db_set import setting
from datetime import timedelta
from models import UsersORM
from fastapi import Response
import bcrypt
import jwt
import datetime

access_token = "acces_token"
refresh_token = "refresh_token"

public_key = setting.public_key.read_text()
private_key = setting.private_key.read_text()

def hash_pass(password : str )->bytes:
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt())

def check_pass(password : str,hash_pass : bytes)->bool:
    return bcrypt.checkpw(password.encode(),hash_pass)

def encode_token(payload : dict,
                 expire_token_time = setting.access_token_time,  
                 expire_token_timedelta : timedelta | None = None):
    
    now = datetime.datetime.utcnow()
    if expire_token_timedelta:
        exp = now + expire_token_timedelta
    else :
        exp = now + timedelta(minutes=expire_token_time)
    payload.update({
        "iat":now,
        "exp":exp
    })
    return jwt.encode(
        payload,
        private_key,
        algorithm= setting.algorithms
    )

def decode_token(token:str):
    return jwt.decode(
        token,
        public_key,
        algorithms= setting.algorithms
    )

def create_token(payload : dict,
                 expire_time : int | None = None,
                 expire_timedelta : int | None = None):
    return encode_token(
        payload= payload.copy(),
        expire_token_time=expire_time,
        expire_token_timedelta=expire_timedelta
    )

def create_access_token(stored_user : UsersORM):
    return create_token(
        payload={
            "token_type":access_token,
            "sub":stored_user.username,
            "user_id":stored_user.id,
            "email":stored_user.email,
            "is_admin":stored_user.is_admin
        },
        expire_time= setting.access_token_time
    )

def create_refresh_token(stored_user: UsersORM):
    return create_token(
        payload={
            "token_type": refresh_token,
            "user_id": stored_user.id,
            "email": stored_user.email,
        },
        expire_timedelta=timedelta(days= setting.refresh_token_time)
    )

def set_cookie(response : Response,key : str,value: str,max_age : int):
    response.set_cookie(
        key= key,
        value= value,
        httponly= True,
        secure= True,
        samesite= "strict",
        max_age= max_age
    )