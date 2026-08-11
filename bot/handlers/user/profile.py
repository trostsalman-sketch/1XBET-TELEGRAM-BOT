from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.repositories import UserRepository

router = Router()

@router.message(Command("profile"))
async def cmd_profile(message: Message, user_repo: UserRepository):
    user = await user_repo.get_by_telegram_id(message.from_user.id)
    
    if not user:
        await message.answer("❌ Пользователь не найден. Используйте /start")
        return
    
    stats = await user_repo.get_stats(user.telegram_id)
    
    profile_text = f"""
👤 ПРОФИЛЬ

🆔 Telegram ID: <code>{user.telegram_id}</code>
👤 Username: @{user.username or 'не указан'}
📅 Регистрация: {user.created_at.strftime('%d.%m.%Y')}

📊 СТАТИСТИКА

🎯 Всего ставок: {stats['total_bets']}
✅ Побед: {stats['wins']}
❌ Поражений: {stats['losses']}
📈 Процент побед: {stats['win_rate']}%
"""
    
    if user.is_blocked:
        profile_text += f"\n🚫 Статус: Заблокирован\nПричина: {user.block_reason}"
    
    await message.answer(profile_text, parse_mode='HTML')
