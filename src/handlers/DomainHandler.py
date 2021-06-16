from src.handlers.handlers import StateHandler
from typing import Tuple, Dict
from definitions import BOT_STATE


class DomainHandler(StateHandler):
    def __init__(self, handlers: Dict[int, StateHandler], state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.handlers = handlers
        self.keywords = {
            'weather': [
                'weather',
                'погода',
                'погоду',
            ],
            'kirill': [
                'аудитория',
            ],
            'dasha': [
                'вино',
            ],
            'goodbye': [
                'пока',
            ]
        }

    def generate_answer(self, msg: str) -> Tuple[int, str]:
        msg = msg.lower()
        words = msg.split()
        weather, kirill, dasha, goodbye = [False] * 4
        for word in words:
            if word in self.keywords['weather']:
                weather = True
            if word in self.keywords['kirill']:
                kirill = True
            if word in self.keywords['dasha']:
                dasha = True
            if word in self.keywords['goodbye']:
                goodbye = True
        if weather + kirill + dasha + goodbye != 1:
            return self.state_id, 'Переформулируй, пожалуйста, я не понял'

        ans = "Whatever"
        next_state = self.state_id

        if kirill:
            next_state, ans = self.handlers[BOT_STATE.KIRILL_DOMAIN.value].generate_answer(msg)
        elif dasha:
            next_state, ans = self.handlers[BOT_STATE.DASHA_DOMAIN.value].generate_answer(msg)
        elif weather:
            next_state, ans = self.handlers[BOT_STATE.WEATHER.value].generate_answer(msg)
        elif goodbye:
            next_state, ans = BOT_STATE.INTRO, 'Пока!'

        return next_state, ans
