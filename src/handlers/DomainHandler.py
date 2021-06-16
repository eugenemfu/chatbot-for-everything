from src.handlers.handlers import StateHandler
from typing import Tuple
from definitions import BOT_STATE


class DomainHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.keywords = dict()
        self.keywords['weather'] = [
            'weather',
            'погода',
            'погоду',
        ]

    def generate_answer(self, msg: str) -> Tuple[int, str]:
        msg = msg.lower()
        words = msg.split()
        weather, kirill, dasha, goodbye = False
        for word in words:
            if word in self.keywords['weather']:
                weather = True
        if weather + kirill + dasha + goodbye != 1:
            return self.state_id, 'Переформулируй, пожалуйста, я не понял'

        ans = "Whatever"

        if kirill:
            next_state = BOT_STATE.KIRILL_DOMAIN
        elif dasha:
            next_state = BOT_STATE.DASHA_DOMAIN
        elif weather:

        elif goodbye:
            next_state = BOT_STATE.INTRO

        return next_state, ans
