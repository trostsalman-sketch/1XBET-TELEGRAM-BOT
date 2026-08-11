from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.repositories import BetRepository

router = Router()

@router.message(Command("history"))
async def cmd_history(message: Message, bet_repo: BetRepository):
    bets = await bet_repo.get_user_history(message.from_user.id, limit=10)
    
    if not bets:
        await message.answer("📭 История ставок пуста.\n\nСоздайте первую ставку командой /stb")
        return
    
    history_text = "📜 ИСТОРИЯ СТАВОК\n\n"
    
    game_icons = {
        'basketball': '🏀',
        'football': '⚽',
        'fortune': '🎡'
    }
    
    status_icons = {
        'pending': '⏳',
        'active': '🎮',
        'won': '✅',
        'lost': '❌',
        'cancelled': '🚫'
    }
    
    for bet in bets:
        game_icon = game_icons.get(bet.game, '🎮')
        status_icon = status_icons.get(bet.status, '❓')
        
        game_name = {
            'basketball': 'Баскетбол',
            'football': 'Футбол',
            'fortune': 'Фортуна'
        }.get(bet.game, bet.game)
        
        status_name = {
            'pending': 'Ожидание оплаты',
            'active': 'Активна',
            'won': 'Победа',
            'lost': 'Проигрыш',
            'cancelled': 'Отменена'
        }.get(bet.status, bet.status)
        
        history_text += f"{game_icon} {game_name} — {bet.amount:,} ₽ — {status_icon} {status_name}\n"
        if bet.result:
            history_text += f"   Результат: {bet.result}\n"
        history_text += f"   {bet.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
    
    await message.answer(history_text)
