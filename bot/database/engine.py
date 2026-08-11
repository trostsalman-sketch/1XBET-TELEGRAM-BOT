from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from bot.config import config

# Создаём URL без sslmode
base_url = "postgresql+asyncpg://neondb_owner:npg_DvgoIX4Ceu9q@ep-flat-recipe-ay2dp5gt-pooler.c-5.us-east-2.aws.neon.tech/neondb"

engine = create_async_engine(
    base_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    connect_args={
        "ssl": "require",  # asyncpg SSL параметр
        "server_settings": {
            "application_name": "xbet_bot"
        }
    }
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
