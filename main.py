from api import registration_router,login_router
from core import async_engine
from models import Base
from fastapi import FastAPI


import uvicorn

app = FastAPI()

@app.on_event("startup")    
async def startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



if __name__ == "__main__":
    uvicorn.run("main:app",host = "127.0.0.1",port=8000)

