from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.engine import async_session_maker
from bot.database.repositories import UserRepository, AdminRepository, BetRepository, AdminLogRepository

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with async_session_maker() as session:
            data['session'] = session
            data['user_repo'] = UserRepository(session)
            data['admin_repo'] = AdminRepository(session)
            data['bet_repo'] = BetRepository(session)
            data['log_repo'] = AdminLogRepository(session)
            
            return await handler(event, data)
