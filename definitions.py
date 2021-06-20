import os
import pandas as pd

from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from typing import Union, List

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# TELEGRAM_TOKEN = "1886759359:AAEk68CWKWjJ_MOw7LnLIEwG4aO-nI71qSY"
TELEGRAM_TOKEN = list(pd.read_csv(Path(ROOT_DIR) / 'data/dasha_token.csv').token_id)[0]



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
    HELLO = ['привет', 'приветик', 'хэй', 'хай', 'hello', 'hey']
    BYE = ['пока', 'встреча', 'связь', 'прощание']
    THANKS = ['спасибо', 'спасибки', 'спасиб', 'thank', 'thanks']
    WEATHER = ['weather', 'погода', 'градус', 'улица']
    KIRILL = ['чгк', 'вопрос', 'что', 'где', 'когда']
    DASHA = ['вино', 'вина', 'винишко', 'выпить', 'сухой', 'сладкий', 'купить', 'розовый']


@unique
class BotVocabulary(Enum):
    INTRO = f'Привет! Я могу посмотреть погоду, cгенерировать оригинальный вопрос в стиле ЧГК или предложить вино ' \
            f'на твой вкус. Могу быть чем-то полезен?'
    GREET = 'Привет! Чем могу помочь?'
    ASK = 'Переформулируй, пожалуйста, я не понял'
    PLEASE = 'Пожалуйста)'
    FAREWELLS = 'Пока! Обращайся если что)'


@dataclass(frozen=True)
class ArgumentInfo:
    user_name: List[str]
    api_code: Union[str, int, List]


@unique
class WineType(Enum):
    RED = ArgumentInfo(['красный'], 1)
    WHITE = ArgumentInfo(['белый'], 2)
    SPARKLING = ArgumentInfo(['игристый', 'шампанское', 'газированный'], 3)
    ROSE = ArgumentInfo(['розовый'], 4)
    DESERT = ArgumentInfo(['десертный'], 5)
    FORTIFIED = ArgumentInfo(['крепленый', 'спиртованный'], 6)


@unique
class WineCountry(Enum):
    ARGENTINE = ArgumentInfo(['аргентина', 'аргентинский', 'argentine', 'argentinean'], 'Argentine')
    AUSTRALIA = ArgumentInfo(['австралия', 'австралийский', 'australian', 'australia'], 'Australia')
    CANADA = ArgumentInfo(['канада', 'канадский', 'canada', 'canadian'], 'Canada')
    CHILE = ArgumentInfo(['чили', 'чилийский', 'chile', 'chilean'], 'Chile')
    FRANCE = ArgumentInfo(['франция', 'фрэнч', 'французский', 'french', 'france'], 'France')
    ITALY = ArgumentInfo(['италия', 'итальянский', 'italian', 'italy'], 'Italy')
    GEORGIA = ArgumentInfo(['грузия', 'грузинский', 'georgia', 'georgian'], 'Georgia')
    MEXICO = ArgumentInfo(['мексика', 'мексиканский', 'mexico', 'mexican'], 'Mexico')
    NEW_ZEALAND = ArgumentInfo(['зеландия', 'зеландский', 'zealand'], 'New Zealand')
    POLAND = ArgumentInfo(['польша', 'польский', 'polish', 'poland'], 'Poland')
    PORTUGAL = ArgumentInfo(['португалия', 'португальский', 'portugal', 'portuguese'], 'Portugal')
    RUSSIA = ArgumentInfo(['россия', 'российский', 'русский', 'russian', 'russia'], 'Russia')
    SPAIN = ArgumentInfo(['испания', 'испанский', 'spain', 'spanish'], 'Spain')
    UKRAINE = ArgumentInfo(['украина', 'украинский', 'ukraine', 'ukrainian'], 'Ukraine')
    USA = ArgumentInfo(['штат', 'соединенный', 'америка', 'us', 'usa', 'america', 'state'], 'USA')


@unique
class AvailableOption(Enum):
    COUNTRIES = ArgumentInfo(
        ['Аргентина', 'Австралия', 'Канада', 'Чили', 'Франция', 'Италия', 'Грузия', 'Мексика', 'Новая Зеландия',
         'Польша', 'Португалия', 'Россия', 'Испания', 'Украина', 'Америка'],
        ['ARGENTINE', 'AUSTRALIA', 'CANADA', 'CHILE', 'FRANCE', 'ITALY', 'GEORGIA', 'MEXICO', 'NEW_ZEALAND',
         'POLAND', 'PORTUGAL', 'RUSSIA', 'SPAIN', 'UKRAINE', 'USA']
    )

    TYPES = ArgumentInfo(
        ['красное', 'белое', 'розовое', 'игристое', 'десертное', 'крепленое'],
        ['RED', 'WHITE', 'SPARKLING', 'ROSE', 'DESERT', 'FORTIFIED']
    )


@unique
class WineBotVocabulary(Enum):
    INTRO = f'Сейчас что-нибудь подберем, только задам пару вопросов. ' \
              f'Какое вино предпочитаем: ' \
              f'{", ".join(str(x) for x in AvailableOption.TYPES.value.user_name[:-1])} ' \
              f'или {AvailableOption.TYPES.value.user_name[-1]}?'

    QUESTION = f'Отлично, теперь давай определимся со страной?'

    ASK = f'Пожалуйста, выбери, что-нибудь из списка: '

    NUMBER = f'Oй, давай одним числом, например: 2000'

    PRICE = f'Вино в какой ценовой категории будем рассматривать? Пожалуйста, укажи одно число – верхнюю границу ' \
            f'диапазона.'

    POSITIVE = f'Да, в моих мечтах за распитие вина тоже платят... но нам нужно положительное число. Попробуй еще раз'


@unique
class ApiArgument(Enum):
    HEADER_USER = "User-Agent"
    HEADER_ADDRESS = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    API_ADDRESS = 'https://www.vivino.com/api/explore/explore'


parameter_dict = params = {"country_code": "ru",
                           "currency_codes[]": "RUB",
                           "min_rating": 1,
                           "page": 1,
                           "price_range_max": 2000,
                           "price_range_min": 250,
                           "wine_type_ids[]": 1}
