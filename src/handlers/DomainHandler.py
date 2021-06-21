from typing import Dict, Union

from src.handlers.handlers import StateHandler
from util import lemmatize
from definitions import BOT_STATE, KeyWords, BotVocabulary


class DomainHandler(StateHandler):
    def __init__(self, handlers: Dict[BOT_STATE, StateHandler], state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.handlers = handlers
        self.keywords = {'weather': KeyWords.WEATHER.value,
                         'kirill': KeyWords.KIRILL.value,
                         'dasha': KeyWords.DASHA.value}

    def generate_answer(self, msg: str, user_id: int) -> Union[int, str]:
        lemmas = lemmatize(msg)

        weather, kirill, dasha = [False] * 3
        for word in lemmas:
            if word in self.keywords['weather']:
                weather = True
            if word in self.keywords['kirill']:
                kirill = True
            if word in self.keywords['dasha']:
                dasha = True
        if weather + kirill + dasha > 1:
            return self.state_id, 'Переформулируй, пожалуйста, я не понял'
        if weather + kirill + dasha == 0:
            return self.state_id, 'Чем я могу помочь?'


        if kirill:
            next_state, ans = self.handlers[BOT_STATE.KIRILL_DOMAIN].generate_answer(msg, user_id)
        elif dasha:
            next_state, ans = self.handlers[BOT_STATE.DASHA_DOMAIN].generate_answer(lemmas, user_id)
        elif weather:
            next_state, ans = self.handlers[BOT_STATE.WEATHER].generate_answer(msg, user_id)

        return next_state, ans
