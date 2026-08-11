from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.database.repositories import UserRepository, AdminLogRepository
from bot.keyboards.admin import get_back_to_admin_kb, get_user_actions_kb

router = Router()

class UserStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_block_reason = State()

@router.callback_query(F.data == "admin:users")
async def admin_users(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.waiting_for_user_id)
    await callback.message.edit_text(
        "👥 УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ\n\n"
        "Отправьте Telegram ID пользователя:",
        reply_markup=get_back_to_admin_kb()
    )
    await callback.answer()

@router.message(UserStates.waiting_for_user_id)
async def process_user_id(message: Message, state: FSMContext, user_repo: UserRepository):
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Неверный формат. Введите числовой Telegram ID.")
        return
    
    user = await user_repo.get_by_telegram_id(user_id)
    
    if not user:
        await message.answer("❌ Пользователь не найден.")
        return
    
    stats = await user_repo.get_stats(user_id)
    
    user_text = f"""
👤 ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ

🆔 ID: <code>{user.telegram_id}</code>
👤 Username: @{user.username or 'не указан'}
📝 Имя: {user.first_name or 'не указано'}
📅 Регистрация: {user.created_at.strftime('%d.%m.%Y %H:%M')}

📊 СТАТИСТИКА
🎯 Ставок: {stats['total_bets']}
✅ Побед: {stats['wins']}
❌ Поражений: {stats['losses']}
📈 Win rate: {stats['win_rate']}%

🚫 Заблокирован: {'Да' if user.is_blocked else 'Нет'}
"""
    
    if user.is_blocked:
        user_text += f"\nПричина: {user.block_reason}"
    
    await message.answer(user_text, parse_mode='HTML', reply_markup=get_user_actions_kb(user_id))
    await state.clear()

@router.callback_query(F.data.startswith("admin:block:"))
async def admin_block_user(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(":")[2])
    await state.update_data(target_user_id=user_id)
    await state.set_state(UserStates.waiting_for_block_reason)
    
    await callback.message.edit_text(
        f"🚫 Блокировка пользователя {user_id}\n\n"
        "Введите причину блокировки:"
    )
    await callback.answer()

@router.message(UserStates.waiting_for_block_reason)
async def process_block_reason(message: Message, state: FSMContext, user_repo: UserRepository, log_repo: AdminLogRepository):
    data = await state.get_data()
    user_id = data['target_user_id']
    reason = message.text.strip()
    
    await user_repo.block_user(user_id, reason, message.from_user.id)
    await log_repo.log(
        admin_id=message.from_user.id,
        action='block_user',
        target_user_id=user_id,
        details={'reason': reason}
    )
    
    await message.answer(f"✅ Пользователь {user_id} заблокирован.")
    await state.clear()

@router.callback_query(F.data.startswith("admin:unblock:"))
async def admin_unblock_user(callback: CallbackQuery, user_repo: UserRepository, log_repo: AdminLogRepository):
    user_id = int(callback.data.split(":")[2])
    
    await user_repo.unblock_user(user_id)
    await log_repo.log(
        admin_id=callback.from_user.id,
        action='unblock_user',
        target_user_id=user_id
    )
    
    await callback.message.edit_text(f"✅ Пользователь {user_id} разблокирован.")
    await callback.answer()
