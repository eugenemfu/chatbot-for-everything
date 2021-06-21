import os
from enum import Enum, unique

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TELEGRAM_TOKEN = "1886759359:AAEk68CWKWjJ_MOw7LnLIEwG4aO-nI71qSY"
WEATHER_TOKEN = "90afa07e-a2d3-4af8-aa37-c8254e7848f6"
WEATHER_API = "https://api.weather.yandex.ru/v2/forecast?"

CHGK_MODEL_PATH = "data/models/new_data/"
TOKENIZER_PATH = "sberbank-ai/rugpt3small_based_on_gpt2"


@unique
class BOT_STATE(Enum):
    INTRO = 0
    DOMAIN_RECOGNITION = 1
    WEATHER = 2
    KIRILL_DOMAIN = 3
    DASHA_DOMAIN = 4


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
    INTRO = f'Привет! Я могу посмотреть погоду, cгенерировать оригинальный вопрос в стиле ЧГК или предложить вино ' \
            f'на твой вкус. Могу быть чем-то полезен?'
    GREET = 'Привет! Чем могу помочь?'
    ASK = 'Переформулируй, пожалуйста, я не понял'
    PLEASE = 'Пожалуйста)'
