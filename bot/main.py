import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import config
from bot.database.engine import engine
from bot.database.models import Base
from bot.middleware.db import DatabaseMiddleware
from bot.middleware.throttling import ThrottlingMiddleware
from bot.handlers import user, admin

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    # Создаём таблицы
    await create_tables()
    
    # Инициализация бота
    bot = Bot(token=config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Подключаем middleware
    dp.update.middleware(DatabaseMiddleware())
    dp.update.middleware(ThrottlingMiddleware())
    
    # Подключаем роутеры
    dp.include_router(user.router)
    dp.include_router(admin.router)
    
    # Инициализируем Owner в БД
    from bot.database.repositories import AdminRepository
    from bot.database.engine import async_session_maker
    
    async with async_session_maker() as session:
        admin_repo = AdminRepository(session)
        if not await admin_repo.is_admin(config.OWNER_ID):
            from bot.database.models import Admin
            owner = Admin(telegram_id=config.OWNER_ID, role='owner', appointed_by=config.OWNER_ID)
            session.add(owner)
            await session.commit()
            logger.info(f"Owner {config.OWNER_ID} initialized")
    
    logger.info("Bot started")
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
