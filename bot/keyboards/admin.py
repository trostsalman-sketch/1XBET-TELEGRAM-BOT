from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_main_kb() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin:users")],
        [InlineKeyboardButton(text="🎯 Ставки", callback_data="admin:bets")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin:stats")],
        [InlineKeyboardButton(text="👮 Администраторы", callback_data="admin:admins")],
        [InlineKeyboardButton(text="🚫 Блокировки", callback_data="admin:blocks")],
        [InlineKeyboardButton(text="📜 Логи", callback_data="admin:logs")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_to_admin_kb() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text="◀️ Назад", callback_data="admin:back")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_management_kb() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="➕ Назначить администратора", callback_data="admin:add_admin")],
        [InlineKeyboardButton(text="➖ Снять администратора", callback_data="admin:remove_admin")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin:back")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_user_actions_kb(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🚫 Заблокировать", callback_data=f"admin:block:{user_id}")],
        [InlineKeyboardButton(text="✅ Разблокировать", callback_data=f"admin:unblock:{user_id}")],
        [InlineKeyboardButton(text="📊 История ставок", callback_data=f"admin:user_bets:{user_id}")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin:users")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
