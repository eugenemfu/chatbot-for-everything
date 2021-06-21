from src.handlers.handlers import StateHandler
from typing import Tuple, Dict
from definitions import BOT_STATE


class DomainHandler(StateHandler):
    def __init__(self, handlers: Dict[BOT_STATE, StateHandler], state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.handlers = handlers
        self.keywords = {
            'weather': [
                'weather',
                'погода',
                'погоду',
            ],
            'kirill': [
                'чгк',
            ],
            'dasha': [
                'вино',
            ],
            'goodbye': [
                'пока',
            ]
        }

    def generate_answer(self, msg: str, user_id: int) -> Tuple[int, str]:
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
        if weather + kirill + dasha + goodbye > 1:
            return self.state_id, 'Переформулируй, пожалуйста, я не понял'
        if weather + kirill + dasha + goodbye == 0:
            return self.state_id, 'Чем я могу помочь?'


        if kirill:
            next_state, ans = self.handlers[BOT_STATE.KIRILL_DOMAIN].generate_answer(msg, user_id)
        elif dasha:
            next_state, ans = self.handlers[BOT_STATE.DASHA_DOMAIN].generate_answer(msg, user_id)
        elif weather:
            next_state, ans = self.handlers[BOT_STATE.WEATHER].generate_answer(msg, user_id)
        elif goodbye:
            next_state, ans = BOT_STATE.INTRO, 'Пока!'

        return next_state, ans
