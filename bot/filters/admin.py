from aiogram.filters import Filter
from aiogram.types import Message
from bot.database.repositories import AdminRepository

class IsAdmin(Filter):
    async def __call__(self, message: Message, admin_repo: AdminRepository) -> bool:
        return await admin_repo.is_admin(message.from_user.id)

class IsOwner(Filter):
    async def __call__(self, message: Message, admin_repo: AdminRepository) -> bool:
        role = await admin_repo.get_role(message.from_user.id)
        return role == 'owner'

class IsPrivateChat(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == 'private'
