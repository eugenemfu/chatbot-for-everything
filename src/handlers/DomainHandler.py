from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from string import punctuation
from typing import Tuple, Dict

from src.handlers.handlers import StateHandler
from definitions import BOT_STATE, KeyWords, BotVocabulary


class DomainHandler(StateHandler):
    def __init__(self, handlers: Dict[BOT_STATE, StateHandler], state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.handlers = handlers
        self.keywords = {'hello': KeyWords.HELLO.value,
                         'weather': KeyWords.WEATHER.value,
                         'kirill': KeyWords.KIRILL.value,
                         'dasha': KeyWords.DASHA.value,
                         'thanks': KeyWords.THANKS.value,
                         'goodbye': KeyWords.BYE.value}

    def generate_answer(self, msg: str, user_id: int) -> Tuple[int, str]:
        msg = msg.lower()
        tokens = word_tokenize(msg)
        # words without punctuation
        filtered_tokens = [w for w in tokens if not w.lower() in punctuation]
        lemmatizer = WordNetLemmatizer()
        # words in infinitive form
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
            if word in self.keywords['thanks']:
                thanks = True
            # users can greet and request at the same time, answer on greeting only if request was not captured
            elif word in self.keywords['hello']:
                hello = True
        if weather + kirill + dasha + goodbye + hello + thanks != 1:
            return self.state_id, BotVocabulary.ASK.value

        ans = "Whatever"
        next_state = self.state_id

        if kirill:
            next_state, ans = self.handlers[BOT_STATE.KIRILL_DOMAIN].generate_answer(msg, user_id)
        elif dasha:
            next_state, ans = self.handlers[BOT_STATE.DASHA_DOMAIN].generate_answer(msg, user_id)
        elif weather:
            next_state, ans = self.handlers[BOT_STATE.WEATHER].generate_answer(msg, user_id)
        elif goodbye:
            next_state, ans = BOT_STATE.INTRO, BotVocabulary.FAREWELLS.value
        elif hello:
            ans = BotVocabulary.GREET.value
        elif thanks:
            ans = BotVocabulary.PLEASE.value

        return next_state, ans
