from src.handlers.handlers import StateHandler
from typing import Tuple
from definitions import BOT_STATE


class WeatherHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)

    def generate_answer(self, msg: str, user_id) -> Tuple[int, str]:
        ans = "Женя пока ничего не сделал :c"
        next_state = self.state_id
        return next_state, ans
