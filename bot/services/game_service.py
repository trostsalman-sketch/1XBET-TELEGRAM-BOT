import random
from typing import Tuple

class GameService:
    @staticmethod
    def play_basketball(choice: str) -> Tuple[str, bool]:
        """
        Баскетбол: ПОПАДАНИЕ или ПРОМАХ
        choice: 'hit' или 'miss'
        Returns: (result, is_win)
        """
        outcomes = ['hit', 'miss']
        result = random.choice(outcomes)
        is_win = result == choice
        
        result_text = "🏀 ПОПАДАНИЕ" if result == 'hit' else "🚫 ПРОМАХ"
        return result_text, is_win
    
    @staticmethod
    def play_football(choice: str) -> Tuple[str, bool]:
        """
        Футбол: ГОЛ или НЕ ГОЛ
        choice: 'goal' или 'no_goal'
        Returns: (result, is_win)
        """
        outcomes = ['goal', 'no_goal']
        result = random.choice(outcomes)
        is_win = result == choice
        
        result_text = "⚽ ГОЛ" if result == 'goal' else "🚫 НЕ ГОЛ"
        return result_text, is_win
    
    @staticmethod
    def play_fortune(choice: str) -> Tuple[str, bool]:
        """
        Фортуна: колесо с секторами 1-10
        choice: '1' до '10'
        Returns: (result, is_win)
        """
        result = str(random.randint(1, 10))
        is_win = result == choice
        
        result_text = f"🎡 Выпал сектор {result}"
        return result_text, is_win
