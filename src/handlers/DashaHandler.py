import requests
import pandas as pd
import random

from src.handlers.handlers import StateHandler
from typing import Tuple
from pathlib import Path
from util import lemmatize, lemmatize_list
from definitions import BOT_STATE, WineCountry, WineType, WineBotVocabulary, ApiArgument, AvailableOption, \
    parameter_dict, ROOT_DIR

from typing import List, Union


class DashaHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.wine_type = None
        self.wine_country = None
        self.upper_price_bound = None
        self.checkpoint = 0
        self.attempts = 1
        self.quotes = list(pd.read_csv(Path(ROOT_DIR) / 'data/wine_quotes.csv')['quote'])

    @staticmethod
    def __define_wine_type(msg):
        if msg in WineType.WHITE.value.user_name:
            return WineType.WHITE.value.api_code
        elif msg in WineType.SPARKLING.value.user_name:
            return WineType.SPARKLING.value.api_code
        elif msg in WineType.ROSE.value.user_name:
            return WineType.ROSE.value.api_code
        elif msg in WineType.DESERT.value.user_name:
            return WineType.DESERT.value.api_code
        elif msg in WineType.FORTIFIED.value.user_name:
            return WineType.FORTIFIED.value.api_code
        else:
            return WineType.RED.value.api_code

    @staticmethod
    def __define_wine_country(word):
        if word in WineCountry.ARGENTINE.value.user_name:
            return WineCountry.ARGENTINE.value.api_code
        elif word in WineCountry.AUSTRALIA.value.user_name:
            return WineCountry.AUSTRALIA.value.api_code
        elif word in WineCountry.CANADA.value.user_name:
            return WineCountry.CANADA.value.api_code
        elif word in WineCountry.CHILE.value.user_name:
            return WineCountry.CHILE.value.api_code
        elif word in WineCountry.FRANCE.value.user_name:
            return WineCountry.FRANCE.value.api_code
        elif word in WineCountry.ITALY.value.user_name:
            return WineCountry.ITALY.value.api_code
        elif word in WineCountry.GEORGIA.value.user_name:
            return WineCountry.GEORGIA.value.api_code
        elif word in WineCountry.CANADA.value.user_name:
            return WineCountry.CANADA.value.api_code
        elif word in WineCountry.MEXICO.value.user_name:
            return WineType.MEXICO.value.api_code
        elif word in WineCountry.NEW_ZEALAND.value.user_name:
            return WineCountry.NEW_ZEALAND.value.api_code
        elif word in WineCountry.POLAND.value.user_name:
            return WineCountry.POLAND.value.api_code
        elif word in WineCountry.PORTUGAL.value.user_name:
            return WineCountry.PORTUGAL.value.api_code
        elif word in WineCountry.RUSSIA.value.user_name:
            return WineCountry.RUSSIA.value.api_code
        elif word in WineCountry.UKRAINE.value.user_name:
            return WineCountry.UKRAINE.value.api_code
        elif word in WineCountry.USA.value.user_name:
            return WineCountry.USA.value.api_code
        elif word in WineCountry.SPAIN.value.user_name:
            return WineCountry.SPAIN.value.api_code

    def __make_get_request(self) -> dict:
        parameter_dict["price_range_max"] = self.upper_price_bound
        parameter_dict["wine_type_ids[]"] = self.wine_type
        parameter_dict["page"] = self.attempts
        r = requests.get(ApiArgument.API_ADDRESS.value,
                         params=parameter_dict,
                         headers={ApiArgument.HEADER_USER.value: ApiArgument.HEADER_ADDRESS.value})
        return r.json()

    @staticmethod
    def __filter_json_results(r: dict) -> pd.DataFrame:
        result_table = [(t['vintage']['name'],
                         t['vintage']['wine']['seo_name'],
                         t["vintage"]["statistics"]["ratings_average"],
                         t["vintage"]["wine"]["region"]["country"]["name"],
                         t['price']['amount'],
                         t["price"]["url"]) for t in r["explore_vintage"]["matches"]]
        dataframe = pd.DataFrame(result_table, columns=['name', 'seo', "rating", "country", "price", "url"])
        return dataframe

    def __generate_answer(self, df: pd.DataFrame):
        df = df[df["country"] == self.wine_country]
        try:
            quote = random.choice(self.quotes)
            ans = f'Предлагаю попробовать {df.name.tolist()[0]}. Рейтинг на Vivno ' \
                  f'{df.rating.tolist()[0]}, в принципе неплохо для {df.price.tolist()[0]} рублей. Заказать' \
                  f' и подробнее ознакомиться с характеристиками можно ознакомиться здесь: {df.url.tolist()[0]}.' \
                  f' Надеюсь, тебе понравится. Твоя цитата дня: {quote}'

        except Exception:
            self.attempts += 1

            if self.attempts < 500:
                r = self.__make_get_request()
                df = self.__filter_json_results(r)
                return self.__generate_answer(df)

            else:
                ans = f"Сложный получился запрос. Я, к сожалению, не смог ничего найти. Попробуешь сначала?"
                self.checkpoint = 0
        return ans

    def get_result(self):
        r = self.__make_get_request()
        df = self.__filter_json_results(r)
        return self.__generate_answer(df)

    def generate_answer(self, msg: Union[List, str], user_id) -> Tuple[int, str]:
        if self.checkpoint == 0:
            self.checkpoint += 1
            return BOT_STATE.DASHA_DOMAIN, WineBotVocabulary.INTRO.value

        elif self.checkpoint == 1:
            types = lemmatize_list(AvailableOption.TYPES.value.user_name)
            msg = lemmatize(msg)
            for word in msg:
                if word in types:
                    self.wine_type = self.__define_wine_type(msg)
                    self.checkpoint += 1
                    ans = WineBotVocabulary.QUESTION.value
                    break
                else:
                    ans = f'{WineBotVocabulary.ASK.value}' \
                          f'{", ".join(str(x) for x in AvailableOption.TYPES.value.user_name[:-1])} ' \
                          f'или {AvailableOption.TYPES.value.user_name[-1]}'
            return BOT_STATE.DASHA_DOMAIN, ans

        elif self.checkpoint == 2:
            countries = lemmatize_list(AvailableOption.COUNTRIES.value.user_name)
            msg = lemmatize(msg)
            for word in msg:
                if word in countries:
                    self.wine_country = self.__define_wine_country(word)
                    self.checkpoint += 1
                    ans = WineBotVocabulary.PRICE.value
                    break
                else:
                    ans = f'{WineBotVocabulary.ASK.value}' \
                          f'{", ".join(str(x) for x in AvailableOption.COUNTRIES.value.user_name[:-1])} ' \
                          f'или {AvailableOption.COUNTRIES.value.user_name[-1]}'
            return BOT_STATE.DASHA_DOMAIN, ans

        elif self.checkpoint == 3:
            try:
                msg = int(msg)
                if msg > 0:
                    self.upper_price_bound = msg
                    self.checkpoint = 0
                    ans = self.get_result()
                else:
                    ans = WineBotVocabulary.POSITIVE.value
            except ValueError:
                ans = WineBotVocabulary.NUMBER.value

        return BOT_STATE.DOMAIN_RECOGNITION, ans
