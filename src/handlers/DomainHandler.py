from src.handlers.handlers import StateHandler
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from string import punctuation
from typing import Tuple, Dict
from definitions import BOT_STATE


class DomainHandler(StateHandler):
    def __init__(self, handlers: Dict[int, StateHandler], state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.handlers = handlers
        self.keywords = {
            'hello': [
                'привет', 'приветик', 'хэй', 'хай', 'hello', 'hey',
            ],
            'weather': [
                'weather', 'погода',
            ],
            'kirill': [
                'чгк', 'вопрос', 'что', 'где', 'когда'
            ],
            'dasha': [
                'вино', 'выпить'
            ],
            'thanks': [
                'спасибо', 'спасибки', 'спасиб', 'thank', 'thanks',
            ],
            'goodbye': [
                'пока',
            ]
        }

    def generate_answer(self, msg: str) -> Tuple[int, str]:
        msg = msg.lower()
        tokens = word_tokenize(msg)
        filtered_tokens = [w for w in tokens if not w.lower() in punctuation]
        lemmatizer = WordNetLemmatizer()
        lemmas = [lemmatizer.lemmatize(w) for w in filtered_tokens]
        weather, kirill, dasha, goodbye, hello, thanks = [False] * 6
        for word in lemmas:
            if word in self.keywords['weather']:
                weather = True
            if word in self.keywords['kirill']:
                kirill = True
            if word in self.keywords['dasha']:
                dasha = True
            if word in self.keywords['goodbye']:
                goodbye = True
            if word in self.keywords['hello']:
                hello = True
            if word in self.keywords['thanks']:
                thanks = True
        if weather + kirill + dasha + goodbye + hello + thanks != 1:
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
            next_state, ans = BOT_STATE.INTRO, 'Пока! Приходи еще :)'
        elif hello:
            ans = 'Привет! Чем могу помочь?'
        if thanks in self.keywords['thanks']:
            ans = 'Пожалуйста :)'

        return next_state, ans
