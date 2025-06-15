from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine,AsyncSession
from db_set import setting

async_engine = create_async_engine(setting.DB_asyncpg)

async_session = async_sessionmaker(async_engine,class_=AsyncSession,expire_on_commit=False)

async def get_db_session():
    async with async_session() as session:
        yield session
        await session.commit()