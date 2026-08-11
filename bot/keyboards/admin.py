from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_main_kb() -> InlineKeyboardMarkup:
    """Главная админ панель"""
    keyboard = [
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin:stats")],
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin:users")],
        [InlineKeyboardButton(text="👮 Администраторы", callback_data="admin:admins")],
        [InlineKeyboardButton(text="🎯 Ставки", callback_data="admin:bets")],
        [InlineKeyboardButton(text="🚫 Блокировки", callback_data="admin:blocks")],
        [InlineKeyboardButton(text="📜 Логи", callback_data="admin:logs")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_panel() -> InlineKeyboardMarkup:
    """Алиас для get_admin_main_kb"""
    return get_admin_main_kb()

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

def get_bet_management_kb(bet_id: int) -> InlineKeyboardMarkup:
    """Управление ставкой"""
    keyboard = [
        [InlineKeyboardButton(text="✅ Одобрить", callback_data=f"admin:approve_bet:{bet_id}")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"admin:reject_bet:{bet_id}")],
        [InlineKeyboardButton(text="🏆 Выигрыш", callback_data=f"admin:win_bet:{bet_id}")],
        [InlineKeyboardButton(text="💔 Проигрыш", callback_data=f"admin:lose_bet:{bet_id}")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin:bets")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_bets_filter_kb() -> InlineKeyboardMarkup:
    """Фильтр ставок"""
    keyboard = [
        [InlineKeyboardButton(text="⏳ Ожидающие", callback_data="admin:bets:pending")],
        [InlineKeyboardButton(text="✅ Одобренные", callback_data="admin:bets:approved")],
        [InlineKeyboardButton(text="🎮 Активные", callback_data="admin:bets:active")],
        [InlineKeyboardButton(text="🏆 Выигрыши", callback_data="admin:bets:won")],
        [InlineKeyboardButton(text="💔 Проигрыши", callback_data="admin:bets:lost")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin:panel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_users_filter_kb() -> InlineKeyboardMarkup:
    """Фильтр пользователей"""
    keyboard = [
        [InlineKeyboardButton(text="👥 Все", callback_data="admin:users:all")],
        [InlineKeyboardButton(text="🚫 Заблокированные", callback_data="admin:users:blocked")],
        [InlineKeyboardButton(text="👮 Администраторы", callback_data="admin:users:admins")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin:panel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cancel_kb() -> InlineKeyboardMarkup:
    """Отмена действия"""
    keyboard = [
        [InlineKeyboardButton(text="❌ Отменить", callback_data="admin:cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_confirm_kb(action: str, target_id: int) -> InlineKeyboardMarkup:
    """Подтверждение действия"""
    keyboard = [
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"admin:confirm:{action}:{target_id}")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="admin:cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
