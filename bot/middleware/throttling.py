from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from cachetools import TTLCache

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, time_limit: float = 1.0):
        self.cache = TTLCache(maxsize=10_000, ttl=time_limit)
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            user_id = event.from_user.id
            
            if user_id in self.cache:
                await event.answer("⏳ Слишком частые запросы. Подождите немного.")
                return
            
            self.cache[user_id] = True
        
        return await handler(event, data)
