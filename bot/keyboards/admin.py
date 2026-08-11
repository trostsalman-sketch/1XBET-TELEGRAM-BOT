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

def get_user_actions_kb(user_id: int, is_blocked: bool = False, is_admin: bool = False) -> InlineKeyboardMarkup:
    """Действия с пользователем"""
    keyboard = []
    
    if is_blocked:
        keyboard.append([InlineKeyboardButton(text="✅ Разблокировать", callback_data=f"admin:unblock:{user_id}")])
    else:
        keyboard.append([InlineKeyboardButton(text="🚫 Заблокировать", callback_data=f"admin:block:{user_id}")])
    
    if is_admin:
        keyboard.append([InlineKeyboardButton(text="➖ Снять админа", callback_data=f"admin:remove_admin:{user_id}")])
    else:
        keyboard.append([InlineKeyboardButton(text="➕ Назначить админом", callback_data=f"admin:add_admin:{user_id}")])
    
    keyboard.append([InlineKeyboardButton(text="💰 Изменить баланс", callback_data=f"admin:balance:{user_id}")])
    keyboard.append([InlineKeyboardButton(text="📜 История ставок", callback_data=f"admin:user_bets:{user_id}")])
    keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data="admin:users")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_user_management_kb(user_id: int, is_blocked: bool = False) -> InlineKeyboardMarkup:
    """Алиас для get_user_actions_kb"""
    return get_user_actions_kb(user_id, is_blocked)

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

def get_bet_actions_kb(bet_id: int, status: str = "pending") -> InlineKeyboardMarkup:
    """Действия со ставкой в зависимости от статуса"""
    keyboard = []
    
    if status == "pending":
        keyboard.append([InlineKeyboardButton(text="✅ Одобрить", callback_data=f"admin:approve_bet:{bet_id}")])
        keyboard.append([InlineKeyboardButton(text="❌ Отклонить", callback_data=f"admin:reject_bet:{bet_id}")])
    elif status == "active":
        keyboard.append([InlineKeyboardButton(text="🏆 Выигрыш", callback_data=f"admin:win_bet:{bet_id}")])
        keyboard.append([InlineKeyboardButton(text="💔 Проигрыш", callback_data=f"admin:lose_bet:{bet_id}")])
    
    keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data="admin:bets")])
    
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

def get_pagination_kb(current_page: int, total_pages: int, prefix: str) -> InlineKeyboardMarkup:
    """Пагинация"""
    keyboard = []
    
    nav_buttons = []
    if current_page > 1:
        nav_buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"{prefix}:page:{current_page-1}"))
    
    nav_buttons.append(InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="ignore"))
    
    if current_page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"{prefix}:page:{current_page+1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data="admin:panel")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
