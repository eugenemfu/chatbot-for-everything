import abc

from typing import Tuple, Iterable
from telegram import Update
from telegram.ext import CallbackContext
from definitions import BOT_STATE


class StateHandler(metaclass=abc.ABCMeta):
    """
    Abstract class for all the handlers.
    """
    def __init__(self, state_id: int):
        self.state_id = state_id

    def __call__(self, update: Update, context: CallbackContext) -> int:
        """
        Each handler is supposed to get a user message from updater, run generate_answer function
         to get an answer and next state id and then return the next state id.
        """
        msg = update.message.text

        next_state, ans = self.generate_answer(msg)

        update.message.reply_text(ans)

        return next_state

    @abc.abstractmethod
    def generate_answer(self, msg: str) -> Tuple[int, str]:
        """
        Generates the answer for user message.
        :param msg: Last message from a user
        :return: Next state and an answer
        """
        raise NotImplementedError()


class IntroHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.INTRO, next_state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.next_state_pos = next_state_id

    def generate_answer(self, msg: str) -> Tuple[int, str]:
        return self.next_state_pos, "Привет! Пока я ничего не знаю, но и Рим не за один день строился."