import abc

from typing import Tuple, Iterable
from telegram import Update
from telegram.ext import CallbackContext
from definitions import BOT_STATE, BotVocabulary
from collections import defaultdict
from util import lemmatize


class StateHandler(metaclass=abc.ABCMeta):
    """
    Abstract class for all the handlers.
    """
    away = defaultdict(bool)
    hello_keywords = [
        'привет',
        'добрый',
        'здравствуйте',
        "здравствовать",
        "приветствовать",
        "здорово",
        "салам",
        "дарова",
        "здарова",
        "хей",
        "хай",
        "хаю",
        "салют",
    ]
    goodbye_keywords = [
        'пока',
        "свидание",
        "до свидания",
        "прощать",
        "прощай",
        "чао",
    ]

    def __init__(self, state_id: int):
        self.state_id = state_id

    def __call__(self, update: Update, context: CallbackContext) -> int:
        """
        Each handler is supposed to get a user message from updater, run generate_answer function
         to get an answer and next state id and then return the next state id.
        """
        msg = update.message.text
        user_id = update.effective_user.id
        words = lemmatize(msg)

        answer = ''

        if StateHandler.away[user_id] or self.check_hello(words):
            answer = 'Привет! '

        if not StateHandler.away[user_id] and self.check_goodbye(words):
            update.message.reply_text("Пока!")
            StateHandler.away[user_id] = True
            return BOT_STATE.DOMAIN_RECOGNITION

        StateHandler.away[user_id] = False

        next_state, ans = self.generate_answer(msg, user_id)

        update.message.reply_text(answer + ans)

        return next_state

    def check_hello(self, words):
        for word in words:
            if word in self.hello_keywords:
                return True
        return False

    def check_goodbye(self, words):
        for word in words:
            if word in self.goodbye_keywords:
                return True
        return False

    @abc.abstractmethod
    def generate_answer(self, msg: str, user_id: int) -> Tuple[int, str]:
        """
        Generates the answer for user message.
        :param user_id: id to identify a user
        :param msg: Last message from a user
        :return: Next state and an answer
        """
        raise NotImplementedError()


class IntroHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.INTRO, next_state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.next_state_pos = next_state_id

    def generate_answer(self, msg: str, user_id: int) -> Tuple[int, str]:
        return self.next_state_pos, BotVocabulary.INTRO.value


class HelpHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.INTRO, next_state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.next_state_pos = next_state_id

    def generate_answer(self, msg: str, user_id: int) -> Tuple[int, str]:
        return self.next_state_pos, BotVocabulary.HELP.value

