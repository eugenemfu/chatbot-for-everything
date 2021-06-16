from src.handlers.handlers import StateHandler
from typing import Tuple, Dict
from definitions import BOT_STATE


class DomainHandler(StateHandler):
    def __init__(self, handlers: Dict[int, StateHandler], state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.handlers = handlers

    def generate_answer(self, msg: str) -> Tuple[int, str]:
        msg = msg.lower()
        if msg == "kirill":
            next_state, ans = self.handlers[BOT_STATE.KIRILL_DOMAIN.value].generate_answer(msg)
        elif msg == "dasha":
            next_state, ans = self.handlers[BOT_STATE.DASHA_DOMAIN.value].generate_answer(msg)
        elif msg == "weather":
            next_state, ans = self.handlers[BOT_STATE.WEATHER.value].generate_answer(msg)
        elif msg == "intro":
            next_state, ans = self.handlers[BOT_STATE.INTRO.value].generate_answer(msg)
        else:
            ans, next_state = "Whatever", self.state_id

        return next_state, ans
