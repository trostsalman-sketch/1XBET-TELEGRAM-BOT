from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_kb() -> InlineKeyboardMarkup:
    """Главное меню"""
    keyboard = [
        [InlineKeyboardButton(text="🎯 Создать ставку", callback_data="create_bet")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="📜 История ставок", callback_data="history")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_game_selection_kb() -> InlineKeyboardMarkup:
    """Выбор игры"""
    keyboard = [
        [InlineKeyboardButton(text="🏀 Баскетбол", callback_data="game:basketball")],
        [InlineKeyboardButton(text="⚽ Футбол", callback_data="game:football")],
        [InlineKeyboardButton(text="🎡 Колесо фортуны", callback_data="game:fortune")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_basketball_choice_kb() -> InlineKeyboardMarkup:
    """Варианты для баскетбола"""
    keyboard = [
        [InlineKeyboardButton(text="🏀 Вариант 1", callback_data="variant:basketball:1")],
        [InlineKeyboardButton(text="🏀 Вариант 2", callback_data="variant:basketball:2")],
        [InlineKeyboardButton(text="🏀 Вариант 3", callback_data="variant:basketball:3")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_games")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_football_choice_kb() -> InlineKeyboardMarkup:
    """Варианты для футбола"""
    keyboard = [
        [InlineKeyboardButton(text="⚽ Вариант 1", callback_data="variant:football:1")],
        [InlineKeyboardButton(text="⚽ Вариант 2", callback_data="variant:football:2")],
        [InlineKeyboardButton(text="⚽ Вариант 3", callback_data="variant:football:3")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_games")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_fortune_choice_kb() -> InlineKeyboardMarkup:
    """Варианты для колеса фортуны"""
    keyboard = [
        [InlineKeyboardButton(text="🎡 Красное", callback_data="variant:fortune:red")],
        [InlineKeyboardButton(text="🎡 Чёрное", callback_data="variant:fortune:black")],
        [InlineKeyboardButton(text="🎡 Зелёное", callback_data="variant:fortune:green")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_games")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_payment_kb(bet_id: int) -> InlineKeyboardMarkup:
    """Подтверждение оплаты"""
    keyboard = [
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"paid:{bet_id}")],
        [InlineKeyboardButton(text="❌ Отменить ставку", callback_data=f"cancel_bet:{bet_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_kb() -> InlineKeyboardMarkup:
    """Кнопка назад"""
    keyboard = [
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cancel_kb() -> InlineKeyboardMarkup:
    """Отмена"""
    keyboard = [
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Дополнительные клавиатуры
def get_basketball_variants_kb() -> InlineKeyboardMarkup:
    """Алиас для get_basketball_choice_kb"""
    return get_basketball_choice_kb()

def get_football_variants_kb() -> InlineKeyboardMarkup:
    """Алиас для get_football_choice_kb"""
    return get_football_choice_kb()

def get_fortune_variants_kb() -> InlineKeyboardMarkup:
    """Алиас для get_fortune_choice_kb"""
    return get_fortune_choice_kb()

def get_payment_confirmation_kb(bet_id: int) -> InlineKeyboardMarkup:
    """Алиас для get_payment_kb"""
    return get_payment_kb(bet_id)

def get_back_button_kb() -> InlineKeyboardMarkup:
    """Алиас для get_back_kb"""
    return get_back_kb()
