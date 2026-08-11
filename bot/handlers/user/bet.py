from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.database.repositories import UserRepository, BetRepository
from bot.keyboards.user import (
    get_game_selection_kb, 
    get_basketball_choice_kb, 
    get_football_choice_kb,
    get_fortune_choice_kb,
    get_payment_kb
)
from bot.services.bet_service import BetService
from bot.config import config

router = Router()

class BetStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_game = State()
    waiting_for_choice = State()
    waiting_for_payment = State()

@router.message(Command("stb"))
async def cmd_bet(message: Message, state: FSMContext, user_repo: UserRepository):
    user = await user_repo.get_by_telegram_id(message.from_user.id)
    
    if user.is_blocked:
        await message.answer(f"🚫 Ваш аккаунт заблокирован.\n\nПричина: {user.block_reason}")
        return
    
    args = message.text.split()
    
    if len(args) < 2:
        await message.answer(
            "Использование: /stb <сумма>\n\n"
            f"Пример: /stb 20000\n\n"
            f"Минимальная ставка: {config.MIN_BET_AMOUNT:,} ₽"
        )
        return
    
    try:
        amount = int(args[1].replace(',', '').replace(' ', ''))
    except ValueError:
        await message.answer("❌ Неверный формат суммы. Используйте числа.")
        return
    
    if amount < config.MIN_BET_AMOUNT:
        await message.answer(f"❌ Минимальная ставка: {config.MIN_BET_AMOUNT:,} ₽")
        return
    
    await state.update_data(amount=amount)
    await state.set_state(BetStates.waiting_for_game)
    
    await message.answer(
        f"💰 Ставка: {amount:,} ₽\n\n"
        "Выберите игру:",
        reply_markup=get_game_selection_kb()
    )

@router.callback_query(F.data.startswith("game:"), BetStates.waiting_for_game)
async def process_game_selection(callback: CallbackQuery, state: FSMContext, bet_repo: BetRepository):
    game = callback.data.split(":")[1]
    data = await state.get_data()
    amount = data['amount']
    
    # Создаём ставку в БД
    bet = await bet_repo.create(
        user_id=callback.from_user.id,
        amount=amount,
        game=game,
        choice=""  # Пока не выбран
    )
    
    await state.update_data(bet_id=bet.id, game=game)
    await state.set_state(BetStates.waiting_for_choice)
    
    game_names = {
        'basketball': '🏀 Баскетбол',
        'football': '⚽ Футбол',
        'fortune': '🎡 Фортуна'
    }
    
    # Выбираем клавиатуру в зависимости от игры
    if game == 'basketball':
        kb = get_basketball_choice_kb(bet.id)
        await callback.message.edit_text(
            f"💰 Ставка: {amount:,} ₽\n"
            f"🎮 Игра: {game_names[game]}\n\n"
            "Выберите вариант:",
            reply_markup=kb
        )
    elif game == 'football':
        kb = get_football_choice_kb(bet.id)
        await callback.message.edit_text(
            f"💰 Ставка: {amount:,} ₽\n"
            f"🎮 Игра: {game_names[game]}\n\n"
            "Выберите вариант:",
            reply_markup=kb
        )
    elif game == 'fortune':
        kb = get_fortune_choice_kb(bet.id)
        await callback.message.edit_text(
            f"💰 Ставка: {amount:,} ₽\n"
            f"🎮 Игра: {game_names[game]}\n\n"
            "Выберите сектор (1-10):",
            reply_markup=kb
        )
    
    await callback.answer()

@router.callback_query(F.data.startswith("choice:"), BetStates.waiting_for_choice)
async def process_choice(callback: CallbackQuery, state: FSMContext, bet_repo: BetRepository):
    parts = callback.data.split(":")
    bet_id = int(parts[1])
    game = parts[2]
    choice = parts[3]
    
    # Обновляем выбор в ставке
    bet = await bet_repo.get_by_id(bet_id)
    if not bet:
        await callback.answer("❌ Ставка не найдена", show_alert=True)
        return
    
    # Сохраняем choice через SQL
    from sqlalchemy import update
    from bot.database.models import Bet
    stmt = update(Bet).where(Bet.id == bet_id).values(choice=choice)
    await bet_repo.session.execute(stmt)
    await bet_repo.session.commit()
    
    await state.update_data(choice=choice)
    await state.set_state(BetStates.waiting_for_payment)
    
    data = await state.get_data()
    amount = data['amount']
    
    choice_text = {
        'hit': '🏀 ПОПАДАНИЕ',
        'miss': '🚫 ПРОМАХ',
        'goal': '⚽ ГОЛ',
        'no_goal': '🚫 НЕ ГОЛ'
    }.get(choice, f'🎡 Сектор {choice}')
    
    await callback.message.edit_text(
        f"✅ Ставка создана!\n\n"
        f"💰 Сумма: {amount:,} ₽\n"
        f"🎯 Ваш выбор: {choice_text}\n\n"
        f"Для активации ставки оплатите {amount:,} ₽ получателю {config.PAYMENT_RECEIVER}.\n\n"
        "После оплаты нажмите '✅ Я оплатил'.",
        reply_markup=get_payment_kb(amount, bet_id)
    )
    
    await callback.answer()

@router.callback_query(F.data.startswith("paid:"))
async def process_payment_confirm(callback: CallbackQuery, state: FSMContext, bet_repo: BetRepository):
    bet_id = int(callback.data.split(":")[1])
    
    bet = await bet_repo.get_by_id(bet_id)
    if not bet or bet.user_id != callback.from_user.id:
        await callback.answer("❌ Ставка не найдена", show_alert=True)
        return
    
    if bet.status != 'pending':
        await callback.answer("❌ Ставка уже обработана", show_alert=True)
        return
    
    # TODO: Здесь должна быть про
