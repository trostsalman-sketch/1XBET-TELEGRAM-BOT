from dataclasses import dataclass
from os import getenv
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # Bot
    BOT_TOKEN: str = getenv("BOT_TOKEN", "")
    OWNER_ID: int = int(getenv("OWNER_ID", "0"))
    
    # Database - приоритет DATABASE_URL
    DATABASE_URL: str = getenv("DATABASE_URL", "")
    
    # Fallback к отдельным переменным
    DB_HOST: str = getenv("DB_HOST", "localhost")
    DB_PORT: str = getenv("DB_PORT", "5432")  # Строка, не int!
    DB_NAME: str = getenv("DB_NAME", "xbet")
    DB_USER: str = getenv("DB_USER", "postgres")
    DB_PASS: str = getenv("DB_PASS", "")
    
    @property
    def database_url(self) -> str:
        # Если есть DATABASE_URL - используем её
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            # Конвертируем postgres:// в postgresql+asyncpg://
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql+asyncpg://", 1)
            elif url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url
        
        # Иначе собираем из отдельных параметров
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Payment
    PAYMENT_RECEIVER: str = getenv("PAYMENT_RECEIVER", "@Msk2314")
    
    # Settings
    MIN_BET_AMOUNT: int = 10_000
    THROTTLE_TIME_USER: float = 1.0
    THROTTLE_TIME_ADMIN: float = 0.5

config = Config()
