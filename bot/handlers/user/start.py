from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.repositories import UserRepository

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, user_repo: UserRepository):
    user = await user_repo.get_or_create(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    await message.answer(
        "👋 Добро пожаловать в 1XBET!\n\n"
        "🎯 Приём ставок открыт.\n\n"
        "Для просмотра команд используйте /helpp"
    )

@router.message(Command("helpp"))
async def cmd_help(message: Message):
    help_text = """
📋 ДОСТУПНЫЕ КОМАНДЫ

/stb <сумма> — создать ставку
/profile — профиль игрока
/history — история ставок
/helpp — помощь

💰 Минимальная ставка: 10,000 ₽

🎮 Доступные игры:
🏀 Баскетбол
⚽ Футбол
🎡 Фортуна
"""
    await message.answer(help_text)
