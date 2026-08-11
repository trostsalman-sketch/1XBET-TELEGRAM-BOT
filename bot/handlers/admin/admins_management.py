from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.filters.admin import IsOwner
from bot.database.repositories import AdminRepository, UserRepository, AdminLogRepository
from bot.keyboards.admin import get_admin_management_kb, get_back_to_admin_kb

router = Router()

class AdminStates(StatesGroup):
    waiting_for_add_admin_id = State()
    waiting_for_remove_admin_id = State()

@router.callback_query(F.data == "admin:admins", IsOwner())
async def admin_admins(callback: CallbackQuery, admin_repo: AdminRepository):
    admins = await admin_repo.get_all()
    
    text = "👮 СПИСОК АДМИНИСТРАТОРОВ\n\n"
    
    for admin in admins:
        role_icon = "👑" if admin.role == 'owner' else "🛡️"
        text += f"{role_icon} ID: {admin.telegram_id} — {admin.role.upper()}\n"
    
    await callback.message.edit_text(text, reply_markup=get_admin_management_kb())
    await callback.answer()

@router.callback_query(F.data == "admin:admins")
async def admin_admins_denied(callback: CallbackQuery):
    await callback.answer("❌ Доступ запрещён. Только для Owner.", show_alert=True)

@router.callback_query(F.data == "admin:add_admin", IsOwner())
async def admin_add_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_add_admin_id)
    await callback.message.edit_text(
        "➕ НАЗНАЧЕНИЕ АДМИНИСТРАТОРА\n\n"
        "Отправьте Telegram ID пользователя:",
        reply_markup=get_back_to_admin_kb()
    )
    await callback.answer()

@router.message(AdminStates.waiting_for_add_admin_id)
async def process_add_admin(message: Message, state: FSMContext, admin_repo: AdminRepository, user_repo: UserRepository, log_repo: AdminLogRepository):
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Неверный формат ID.")
        return
    
    user = await user_repo.get_by_telegram_id(user_id)
    if not user:
        await message.answer("❌ Пользователь не найден в системе.")
        return
    
    if await admin_repo.is_admin(user_id):
        await message.answer("❌ Пользователь уже является администратором.")
        return
    
    await admin_repo.add_admin(user_id, message.from_user.id)
    await log_repo.log(
        admin_id=message.from_user.id,
        action='add_admin',
        target_user_id=user_id
    )
    
    await message.answer(f"✅ Пользователь {user_id} назначен администратором.")
    await state.clear()

@router.callback_query(F.data == "admin:remove_admin", IsOwner())
async def admin_remove_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_remove_admin_id)
    await callback.message.edit_text(
        "➖ СНЯТИЕ АДМИНИСТРАТОРА\n\n"
        "Отправьте Telegram ID администратора:",
        reply_markup=get_back_to_admin_kb()
    )
    await callback.answer()

@router.message(AdminStates.waiting_for_remove_admin_id)
async def process_remove_admin(message: Message, state: FSMContext, admin_repo: AdminRepository, log_repo: AdminLogRepository):
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Неверный формат ID.")
        return
    
    role = await admin_repo.get_role(user_id)
    
    if not role:
        await message.answer("❌ Пользователь не является администратором.")
        return
    
    if role == 'owner':
        await message.answer("❌ Нельзя снять Owner.")
        return
    
    await admin_repo.remove_admin(user_id)
    await log_repo.log(
        admin_id=message.from_user.id,
        action='remove_admin',
        target_user_id=user_id
    )
    
    await message.answer(f"✅ Администратор {user_id} снят с должности.")
    await state.clear()
