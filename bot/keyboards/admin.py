from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_panel() -> InlineKeyboardMarkup:
    """Админ панель"""
    keyboard = [
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin:stats")],
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin:users")],
        [InlineKeyboardButton(text="👮 Администраторы", callback_data="admin:admins")],
        [InlineKeyboardButton(text="🎯 Ставки", callback_data="admin:bets")],
        [InlineKeyboardButton(text="🚫 Блокировки", callback_data="admin:blocks")],
        [InlineKeyboardButton(text="📜 Логи", callback_data="admin:logs")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_to_admin_kb() -> InlineKeyboardMarkup:
    """Назад в админ панель"""
    keyboard = [
        [InlineKeyboardButton(text="◀️ Назад в админ-панель", callback_data="admin:panel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_user_management_kb(user_id: int, is_blocked: bool = False) -> InlineKeyboardMarkup:
    """Управление пользователем"""
    keyboard = []
    
    if is_blocked:
        keyboard.append([InlineKeyboardButton(text="✅ Разблокировать", callback_data=f"admin:unblock:{user_id}")])
    else:
        keyboard.append([InlineKeyboardButton(text="🚫 Заблокировать", callback_data=f"admin:block:{user_id}")])
    
    keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data="admin:users")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_management_kb() -> InlineKeyboardMarkup:
    """Управление администраторами"""
    keyboard = [
        [InlineKeyboardButton(text="➕ Назначить администратора", callback_data="admin:add_admin")],
        [InlineKeyboardButton(text="➖ Снять администратора", callback_data="admin:remove_admin")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin:panel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cancel_kb() -> InlineKeyboardMarkup:
    """Отмена действия"""
    keyboard = [
        [InlineKeyboardButton(text="❌ Отменить", callback_data="admin:cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
