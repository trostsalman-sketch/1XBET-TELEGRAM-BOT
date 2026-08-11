from dataclasses import dataclass
from os import getenv
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

@dataclass
class Config:
    # Bot
    BOT_TOKEN: str = getenv("BOT_TOKEN", "")
    OWNER_ID: int = int(getenv("OWNER_ID", "0"))
    
    @property
    def database_url(self) -> str:
        # Захардкоженный URL
        url = "postgresql://neondb_owner:npg_DvgoIX4Ceu9q@ep-flat-recipe-ay2dp5gt-pooler.c-5.us-east-2.aws.neon.tech/neondb"
        
        # Конвертируем в asyncpg формат
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        
        # Добавляем SSL параметр правильно для asyncpg
        url += "?ssl=require"
        
        return url
    
    # Payment
    PAYMENT_RECEIVER: str = "@Msk2314"
    
    # Settings
    MIN_BET_AMOUNT: int = 10_000
    THROTTLE_TIME_USER: float = 1.0
    THROTTLE_TIME_ADMIN: float = 0.5

config = Config()
