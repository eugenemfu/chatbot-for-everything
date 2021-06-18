from typing import Tuple
import torch

from src.handlers.handlers import StateHandler
from definitions import BOT_STATE, CHGK_MODEL_PATH
from chgk.src.generation.generate import generate, SBER_MODEL_SMALL
from chgk.src.training.models.GPT2SberSmall import GPT2SberSmall


class KirillHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.KIRILL_DOMAIN):
        super().__init__(state_id)
        self.asked_for_context = False

        self.model = GPT2SberSmall(CHGK_MODEL_PATH, SBER_MODEL_SMALL, torch.device("cpu"))
        self.model.eval()

        self.generation_params = {
            "model": self.model,
            "model_dir": CHGK_MODEL_PATH,
            "tokenizer_path": SBER_MODEL_SMALL,
            "max_len": 100,
            "beam_size": 5,
        }

    def generate_answer(self, msg: str) -> Tuple[int, str]:
        if not self.asked_for_context:
            ans = "Хорошо, введите начало вопроса."
            next_state = self.state_id
        else:
            ans, _ = generate(context=msg, **self.generation_params)
            next_state = BOT_STATE.DOMAIN_RECOGNITION.value

        return next_state, ans
