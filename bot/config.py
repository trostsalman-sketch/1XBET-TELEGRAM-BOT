from dataclasses import dataclass
from os import getenv

@dataclass
class Config:
    # Bot
    BOT_TOKEN: str = getenv("BOT_TOKEN", "")
    OWNER_ID: int = int(getenv("OWNER_ID", "0"))
    
    @property
    def database_url(self) -> str:
        # ВРЕМЕННО: захардкоженный URL
        return "postgresql+asyncpg://neondb_owner:npg_DvgoIX4Ceu9q@ep-flat-recipe-ay2dp5gt-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require"
    
    # Payment
    PAYMENT_RECEIVER: str = "@Msk2314"
    
    # Settings
    MIN_BET_AMOUNT: int = 10_000
    THROTTLE_TIME_USER: float = 1.0
    THROTTLE_TIME_ADMIN: float = 0.5

config = Config()
