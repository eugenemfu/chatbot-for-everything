from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Union

from util import translate_list_to_str


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
    COUNTRIES = ['аргентина', 'аргентинский', 'argentine', 'argentinean', 'австралия', 'австралийский', 'australian',
                 'australia', 'канада', 'канадский', 'canada', 'canadian', 'чили', 'чилийский', 'chile', 'chilean',
                 'франция', 'фрэнч', 'французский', 'french', 'france', 'италия', 'итальянский', 'italian', 'italy',
                 'грузия', 'грузинский', 'georgia', 'georgian', 'мексика', 'мексиканский', 'mexico', 'mexican',
                 'зеландия', 'зеландский', 'zealand', 'польша', 'польский', 'polish', 'poland', 'португалия',
                 'португальский', 'portugal', 'portuguese', 'россия', 'российский', 'русский', 'russian', 'russia',
                 'испания', 'испанский', 'spain', 'spanish', 'украина', 'украинский', 'ukraine', 'ukrainian', 'штат',
                 'соединенный', 'америка', 'us', 'usa', 'america', 'state']

    TYPES = ArgumentInfo(
        ['красное', 'белое', 'розовое', 'игристое', 'десертное', 'крепленое'],
        ['RED', 'WHITE', 'SPARKLING', 'ROSE', 'DESERT', 'FORTIFIED']
    )


@unique
class WineBotVocabulary(Enum):
    INTRO = f'Сейчас что-нибудь подберем, только задам пару вопросов. Какое вино предпочитаем: ' \
            f'{translate_list_to_str(AvailableOption.TYPES.value.user_name)} ' \
            f'или {AvailableOption.TYPES.value.user_name[-1]}?'

    QUESTION = 'Отлично, теперь давай определимся со страной?'

    ASK = 'Пожалуйста, выбери, что-нибудь из списка: '

    NUMBER = 'Oй, давай одним числом, например: 2000'

    PRICE = 'Вино в какой ценовой категории будем рассматривать? Пожалуйста, укажи одно число – верхнюю границу ' \
            'диапазона.'

    POSITIVE = 'Да, в моих мечтах за распитие вина тоже платят... но нам нужно положительное число. Попробуй еще раз'

    FAIL = 'Сложный получился запрос. Я, к сожалению, не смог ничего найти. Попробуешь сначала?'


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
