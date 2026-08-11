from dataclasses import dataclass
from os import getenv

@dataclass
class Config:
    # Bot
    BOT_TOKEN: str = getenv("BOT_TOKEN", "")
    OWNER_ID: int = int(getenv("OWNER_ID", "0"))
    
    # Database
    DATABASE_URL: str = getenv("DATABASE_URL", "")
    
    @property
    def database_url(self) -> str:
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")
        
        url = self.DATABASE_URL
        
        # Конвертируем postgres:// в postgresql+asyncpg://
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        
        return url
    
    # Payment
    PAYMENT_RECEIVER: str = getenv("PAYMENT_RECEIVER", "@Msk2314")
    
    # Settings
    MIN_BET_AMOUNT: int = 10_000
    THROTTLE_TIME_USER: float = 1.0
    THROTTLE_TIME_ADMIN: float = 0.5

config = Config()
