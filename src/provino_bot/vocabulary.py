from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Union

from util import translate_list_to_str


@dataclass(frozen=True)
class ArgumentInfo:
    user_name: List[str]
    api_code: Union[str, int, List]


@dataclass(frozen=True)
class ArgumentFullInfo:
    user_name: List[str]
    api_long_name: Union[str, int, List]
    api_short_code: Union[str, List]


@unique
class WineType(Enum):
    RED = ArgumentInfo(["красный"], 1)
    WHITE = ArgumentInfo(["белый"], 2)
    SPARKLING = ArgumentInfo(["игристый", "шампанское", "газированный"], 3)
    ROSE = ArgumentInfo(["розовый"], 4)
    DESERT = ArgumentInfo(["десертный"], 5)
    FORTIFIED = ArgumentInfo(["крепленый", "спиртованный"], 6)


@unique
class WineCountry(Enum):
    ARGENTINE = ArgumentFullInfo(["аргентина", "аргентинский", "argentine", "argentinean"], "Argentine", "ar")
    AUSTRALIA = ArgumentFullInfo(["австралия", "австралийский", "australian", "australia"], "Australia", "au")
    CANADA = ArgumentFullInfo(["канада", "канадский", "canada", "canadian"], "Canada", "ca")
    CHILE = ArgumentFullInfo(["чили", "чилийский", "chile", "chilean"], "Chile", "cl")
    FRANCE = ArgumentFullInfo(["франция", "фрэнч", "французский", "french", "france"], "France", "fr")
    ITALY = ArgumentFullInfo(["италия", "итальянский", "italian", "italy"], "Italy", "it")
    GEORGIA = ArgumentFullInfo(["грузия", "грузинский", "georgia", "georgian"], "Georgia", "ge")
    MEXICO = ArgumentFullInfo(["мексика", "мексиканский", "mexico", "mexican"], "Mexico", "mx")
    NEW_ZEALAND = ArgumentFullInfo(["зеландия", "зеландский", "zealand"], "New Zealand", "nz")
    POLAND = ArgumentFullInfo(["польша", "польский", "polish", "poland"], "Poland", "pl")
    PORTUGAL = ArgumentFullInfo(["португалия", "португальский", "portugal", "portuguese"], "Portugal", "pt")
    RUSSIA = ArgumentFullInfo(["россия", "российский", "русский", "russian", "russia"], "Russia", "ru")
    SPAIN = ArgumentFullInfo(["испания", "испанский", "spain", "spanish"], "Spain", "es")
    UKRAINE = ArgumentFullInfo(["украина", "украинский", "ukraine", "ukrainian"], "Ukraine", "ua")
    USA = ArgumentFullInfo(["штат", "соединенный", "америка", "us", "usa", "america", "state"], "USA", "us")


@unique
class AvailableOption(Enum):
    COUNTRIES = ArgumentInfo(
        [
            "аргентина",
            "аргентинский",
            "argentine",
            "argentinean",
            "австралия",
            "австралийский",
            "australian",
            "australia",
            "канада",
            "канадский",
            "canada",
            "canadian",
            "чили",
            "чилийский",
            "chile",
            "chilean",
            "франция",
            "фрэнч",
            "французский",
            "french",
            "france",
            "италия",
            "итальянский",
            "italian",
            "italy",
            "грузия",
            "грузинский",
            "georgia",
            "georgian",
            "мексика",
            "мексиканский",
            "mexico",
            "mexican",
            "зеландия",
            "зеландский",
            "zealand",
            "польша",
            "польский",
            "polish",
            "poland",
            "португалия",
            "португальский",
            "portugal",
            "portuguese",
            "россия",
            "российский",
            "русский",
            "russian",
            "russia",
            "испания",
            "испанский",
            "spain",
            "spanish",
            "украина",
            "украинский",
            "ukraine",
            "ukrainian",
            "штат",
            "соединенный",
            "америка",
            "us",
            "usa",
            "america",
            "state",
        ],
        [
            "Аргентина",
            "Австралия",
            "Канада",
            "Чили",
            "Франция",
            "Италия",
            "Грузия",
            "Мексика",
            "Новая Зеландия",
            "Польша",
            "Португалия",
            "Россия",
            "Испания",
            "Украина",
            "Америка",
        ],
    )

    TYPES = ArgumentInfo(
        ["красное", "белое", "розовое", "игристое", "десертное", "крепленое"],
        ["RED", "WHITE", "SPARKLING", "ROSE", "DESERT", "FORTIFIED"],
    )

    AGREEMENT = ArgumentInfo(
        ["да", "конечно", "офкос", "yes", "yep", "sure", "ага", "давай", "course", "угу", "ес", "ок", "окей", "еще"],
        ["не", "нет", "no", "ноу", "все"],
    )

    GENERAL = ArgumentFullInfo(
        ["Как на счет", "Можно попробовать", "Предлагаю попробовать", "Еще один вариант –"],
        ["К сожалению, кроме цитаты дня мне больше нечего предложить по этому запросу:"],
        ["Посмотреть еще?", "Смотрим дальше?", "Показать другое?", "Будем дальше смотреть?"],
    )


@unique
class SweetnessDetector(Enum):
    SWEET = ArgumentInfo(["сладко", "сладкий", "сладость"], ["sweet"])

    DRY = ArgumentInfo(["сухой"], ["dry"])


@unique
class WineBotVocabulary(Enum):
    INTRO = (
        f"Сейчас что-нибудь подберем, только задам пару вопросов. Какое вино предпочитаем: "
        f"{translate_list_to_str(AvailableOption.TYPES.value.user_name)}?"
    )

    QUESTION = "Отлично, теперь давай определимся со страной?"

    ASK = "Пожалуйста, выбери, что-нибудь из списка: "

    NUMBER = "Oй, давай одним числом, например: 2000"

    PRICE = (
        "Вино в какой ценовой категории будем рассматривать? Пожалуйста, укажи одно число – верхнюю границу "
        "диапазона."
    )

    POSITIVE = "Да, в моих мечтах за распитие вина тоже платят... но нам нужно положительное число. Попробуй еще раз"

    FAIL = "Сложный получился запрос. Я, к сожалению, не смог ничего найти. Попробуешь сначала?"


@unique
class ApiArgument(Enum):
    HEADER_USER = "User-Agent"
    HEADER_ADDRESS = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    API_ADDRESS = "https://www.vivino.com/api/explore/explore"


parameter_dict = params = {
    "country_code": "ru",
    "currency_codes[]": "RUB",
    "country_codes[]": "fr",
    "min_rating": 1,
    "page": 1,
    "price_range_max": 2000,
    "price_range_min": 250,
    "wine_type_ids[]": 1,
}
