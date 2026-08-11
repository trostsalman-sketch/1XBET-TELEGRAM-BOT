from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.database.repositories import UserRepository, BetRepository
from bot.keyboards.admin import get_back_to_admin_kb

router = Router()

@router.callback_query(F.data == "admin:stats")
async def admin_stats(callback: CallbackQuery, user_repo: UserRepository, bet_repo: BetRepository):
    total_users = await user_repo.count_all()
    total_bets = await bet_repo.count_all()
    pending_bets = await bet_repo.count_by_status('pending')
    active_bets = await bet_repo.count_by_status('active')
    won_bets = await bet_repo.count_by_status('won')
    lost_bets = await bet_repo.count_by_status('lost')
    cancelled_bets = await bet_repo.count_by_status('cancelled')
    total_amount = await bet_repo.get_total_amount()
    
    game_stats = await bet_repo.get_game_stats()
    
    stats_text = f"""
📊 СТАТИСТИКА ПРОЕКТА

👥 ПОЛЬЗОВАТЕЛИ
Всего: {total_users}

🎯 СТАВКИ
Всего: {total_bets}
⏳ Ожидают оплаты: {pending_bets}
🎮 Активных: {active_bets}
✅ Выигрышей: {won_bets}
❌ Проигрышей: {lost_bets}
🚫 Отменено: {cancelled_bets}

💰 ФИНАНСЫ
Общая сумма ставок: {total_amount:,} ₽

🎮 ПО ИГРАМ

🏀 Баскетбол
   Всего: {game_stats['basketball']['total']}
   Выигрыши: {game_stats['basketball']['won']}
   Проигрыши: {game_stats['basketball']['lost']}

⚽ Футбол
   Всего: {game_stats['football']['total']}
   Выигрыши: {game_stats['football']['won']}
   Проигрыши: {game_stats['football']['lost']}

🎡 Фортуна
   Всего: {game_stats['fortune']['total']}
   Выигрыши: {game_stats['fortune']['won']}
   Проигрыши: {game_stats['fortune']['lost']}
"""
    
    await callback.message.edit_text(stats_text, reply_markup=get_back_to_admin_kb())
    await callback.answer()

@router.callback_query(F.data == "admin:bets")
async def admin_bets(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎯 УПРАВЛЕНИЕ СТАВКАМИ\n\n"
        "Этот раздел находится в разработке.\n"
        "Здесь будет отображаться список активных ставок.",
        reply_markup=get_back_to_admin_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "admin:blocks")
async def admin_blocks(callback: CallbackQuery):
    await callback.message.edit_text(
        "🚫 БЛОКИРОВКИ\n\n"
        "Для блокировки пользователя используйте раздел 'Пользователи'.",
        reply_markup=get_back_to_admin_kb()
    )
    await callback.answer()
