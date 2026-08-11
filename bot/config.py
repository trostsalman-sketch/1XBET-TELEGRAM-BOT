from dataclasses import dataclass
from os import getenv
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # Bot
    BOT_TOKEN: str = getenv("BOT_TOKEN", "")
    OWNER_ID: int = int(getenv("OWNER_ID", "0"))
    
    # Database
    DB_HOST: str = getenv("DB_HOST", "localhost")
    DB_PORT: int = int(getenv("DB_PORT", "5432"))
    DB_NAME: str = getenv("DB_NAME", "xbet")
    DB_USER: str = getenv("DB_USER", "postgres")
    DB_PASS: str = getenv("DB_PASS", "")
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Redis
    REDIS_HOST: str = getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(getenv("REDIS_PORT", "6379"))
    
    # Payment
    PAYMENT_RECEIVER: str = getenv("PAYMENT_RECEIVER", "@Msk2314")
    
    # Settings
    MIN_BET_AMOUNT: int = 10_000
    THROTTLE_TIME_USER: float = 1.0
    THROTTLE_TIME_ADMIN: float = 0.5

config = Config()
