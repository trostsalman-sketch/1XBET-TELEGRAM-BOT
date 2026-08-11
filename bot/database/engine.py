from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from bot.config import config

engine = create_async_engine(
    config.database_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
