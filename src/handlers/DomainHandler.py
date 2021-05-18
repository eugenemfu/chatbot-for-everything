from src.handlers.handlers import StateHandler
from typing import Tuple
from definitions import BOT_STATE


class DomainHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)

    def generate_answer(self, msg: str) -> Tuple[int, str]:
        msg = msg.lower()
        if msg == "kirill":
            next_state = BOT_STATE.KIRILL_DOMAIN
        elif msg == "dasha":
            next_state = BOT_STATE.DASHA_DOMAIN
        elif msg == "weather":
            next_state = BOT_STATE.WEATHER
        elif msg == "intro":
            next_state = BOT_STATE.INTRO
        else:
            next_state = self.state_id
        ans = "Whatever"
        return next_state, ans
