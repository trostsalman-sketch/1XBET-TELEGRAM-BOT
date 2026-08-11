from bot.database.repositories import BetRepository
from bot.services.game_service import GameService
from bot.config import config

class BetService:
    def __init__(self, bet_repo: BetRepository):
        self.bet_repo = bet_repo
        self.game_service = GameService()
    
    async def create_bet(self, user_id: int, amount: int, game: str, choice: str):
        if amount < config.MIN_BET_AMOUNT:
            raise ValueError(f"Минимальная ставка: {config.MIN_BET_AMOUNT:,} ₽")
        
        bet = await self.bet_repo.create(user_id, amount, game, choice)
        return bet
    
    async def play_bet(self, bet_id: int):
        bet = await self.bet_repo.get_by_id(bet_id)
        
        if not bet or bet.status != 'active':
            return None
        
        # Определяем игру и играем
        if bet.game == 'basketball':
            result, is_win = self.game_service.play_basketball(bet.choice)
        elif bet.game == 'football':
            result, is_win = self.game_service.play_football(bet.choice)
        elif bet.game == 'fortune':
            result, is_win = self.game_service.play_fortune(bet.choice)
        else:
            return None
        
        status = 'won' if is_win else 'lost'
        await self.bet_repo.complete_bet(bet_id, result, status)
        
        return {
            'result': result,
            'is_win': is_win,
            'status': status
        }
