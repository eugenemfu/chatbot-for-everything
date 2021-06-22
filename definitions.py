import os
from enum import Enum, unique

from tokens import TELEGRAM_TOKEN, WEATHER_TOKEN

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

WEATHER_API = "https://api.weather.yandex.ru/v2/forecast?"

CHGK_MODEL_PATH = "data/models/blitz/"
TOKENIZER_PATH = "sberbank-ai/rugpt3small_based_on_gpt2"


@unique
class BOT_STATE(Enum):
    INTRO = 0
    DOMAIN_RECOGNITION = 1
    WEATHER = 2
    KIRILL_DOMAIN = 3
    DASHA_DOMAIN = 4
    HELP = 5


@unique
class SpecialTokens(Enum):
    PAD = "<pad>"
    BOS = "<s>"
    EOS = "</s>"
    UNK = "<unk>"


@unique
class KeyWords(Enum):
    THANKS = ['спасибо', 'спасибки', 'спасиб', 'thank', 'thanks']
    WEATHER = ['weather', 'погода', 'градус', 'улица']
    KIRILL = ['чгк', 'вопрос', 'где', 'когда']
    DASHA = ['вино', 'вина', 'винишко', 'выпить', 'сухой', 'сладкий', 'купить', 'розовый']


@unique
class BotVocabulary(Enum):
    HELP = f'Я могу посмотреть погоду, cгенерировать оригинальный вопрос в стиле ЧГК или предложить вино ' \
           f'на твой вкус. Могу быть чем-то полезен?'
    INTRO = f'Привет! ' + HELP
    GREET = 'Привет! Чем могу помочь?'
    ASK = 'Переформулируй, пожалуйста, я не понял'
    ASK_HELP = 'Чем я могу помочь? Если хочешь узнать, что я умею, нажми /help'
