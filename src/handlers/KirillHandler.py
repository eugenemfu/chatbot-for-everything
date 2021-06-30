import os
import torch

from transformers import GPT2LMHeadModel, GPT2Tokenizer
from typing import Tuple

from src.handlers.handlers import StateHandler
from definitions import BOT_STATE, SpecialTokens, TOKENIZER_PATH, CHGK_MODEL_PATH, ROOT_DIR


class GPT2SberAbstract(torch.nn.Module):
    def __init__(self, model_dir: str, tokenizer_path: str, device: torch.device):
        super().__init__()
        self.model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained(model_dir)
        self.tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)

        self.model.to(device)
        self.device = device

        self.tokenizer.pad_token = SpecialTokens.PAD.value
        self.tokenizer.bos_token = SpecialTokens.BOS.value
        self.tokenizer.eos_token = SpecialTokens.EOS.value

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

    def forward(self, *args, **kwargs):
        return self.model.forward(*args, **kwargs)

    @torch.no_grad()
    def generate(
        self,
        context: str,
        max_length: int = 100,
        beam_size: int = 5,
        sampling: bool = True,
        top_k: int = 50,
        top_p: float = 0.9,
    ):
        input_ids = self._pre_example(context)

        if not sampling:
            generated_text = self._generate_beam(input_ids, max_length, beam_size)
        else:
            generated_text = self._generate_sampling(input_ids, max_length, top_k, top_p)

        generated_text = self._post_example(generated_text)

        return generated_text

    def _generate_beam(self, input_ids, max_length: int, beam_size: int) -> str:
        greedy_output = self.model.generate(
            input_ids, max_length=max_length, beam_size=beam_size, no_repeat_ngram_size=2, early_stopping=True
        )
        generated_output = self.tokenizer.decode(greedy_output[0], skip_special_tokens=True)

        return generated_output

    def _generate_sampling(self, input_ids, max_length: int, top_k: int = 50, top_p: float = 0.9):
        sampling_output = self.model.generate(
            input_ids, do_sample=True, max_length=max_length, top_k=top_k, top_p=top_p
        )
        generated_output = self.tokenizer.decode(sampling_output[0], skip_special_tokens=True)

        return generated_output

    def _pre_example(self, example) -> torch.LongTensor:
        ...

    def _post_example(self, generated_text) -> str:
        ...


class GPT2SberSimple(GPT2SberAbstract):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _pre_example(self, example) -> torch.LongTensor:
        example = SpecialTokens.BOS.value + " " + example
        input_ids = self.tokenizer.encode(example, return_tensors="pt").to(self.device)

        return input_ids

    def _post_example(self, generated_text) -> str:
        eos_ind = generated_text.find("</s")
        if eos_ind == -1:
            eos_ind = None

        bos_len = len(SpecialTokens.BOS.value) + 1
        generated_text = generated_text[bos_len:eos_ind]

        return generated_text


class KirillHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.KIRILL_DOMAIN):
        super().__init__(state_id)
        self.asked_for_context = False

        self.model = GPT2SberSimple(os.path.join(ROOT_DIR, CHGK_MODEL_PATH), TOKENIZER_PATH, torch.device("cpu"))
        self.model.eval()

        self.generation_params = {
            "max_length": 100,
            "beam_size": 5,
        }

    def generate_answer(self, msg: str, user_id: int) -> Tuple[int, str]:
        if not self.asked_for_context:
            ans = "Хорошо, введите начало вопроса."
            next_state = self.state_id

            self.asked_for_context = True
        else:
            ans = self.model.generate(context=msg, **self.generation_params)
            next_state = BOT_STATE.DOMAIN_RECOGNITION

            self.asked_for_context = False

        return next_state, ans
