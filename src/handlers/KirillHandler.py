from src.handlers.handlers import StateHandler
from typing import Tuple
from definitions import BOT_STATE


class KirillHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.KIRILL_DOMAIN):
        super().__init__(state_id)

    def generate_answer(self, msg: str) -> Tuple[int, str]:
        ans = "Кирилл пока ничего не сделал :c"
        next_state = self.state_id
        return next_state, ans
