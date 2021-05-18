from src.handlers.handlers import StateHandler
from typing import Tuple
from definitions import BOT_STATE


class DashaHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.DASHA_DOMAIN):
        super().__init__(state_id)

    def generate_answer(self, msg: str) -> Tuple[int, str]:
        ans = "Даша пока ничего не сделала :c"
        next_state = self.state_id
        return next_state, ans