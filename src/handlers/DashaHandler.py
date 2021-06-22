from dataclasses import dataclass

import requests
import pandas as pd
import random
import emoji
from typing import Tuple, List, Union
from pathlib import Path

from definitions import BOT_STATE, ROOT_DIR, BotVocabulary
from src.common.wine.vocabulary import WineBotVocabulary, ApiArgument, AvailableOption, parameter_dict
from src.common.wine.msg_interpreter import WineBotInterpreter
from src.handlers.handlers import StateHandler
from util import translate_list_to_str
from util import lemmatize, lemmatize_list


@dataclass
class User:
    wine_type = None
    wine_country = None
    upper_price_bound = None
    country_code = None
    checkpoint = 0
    attempts = 0


class DashaHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.users = {}
        self.df = None
        self.quotes = list(pd.read_csv(Path(ROOT_DIR) / "data/wine_quotes.csv")["quote"])

    def __make_get_request(self, upper_price_bound, wine_type, attempts, country_code) -> dict:
        parameter_dict["price_range_max"] = upper_price_bound
        parameter_dict["wine_type_ids[]"] = wine_type
        parameter_dict["page"] = attempts
        parameter_dict["country_codes[]"] = country_code

        r = requests.get(
            ApiArgument.API_ADDRESS.value,
            params=parameter_dict,
            headers={ApiArgument.HEADER_USER.value: ApiArgument.HEADER_ADDRESS.value},
        )
        return r.json()

    @staticmethod
    def __filter_json_results(r: dict) -> pd.DataFrame:
        result_table = [
            (
                t["vintage"]["name"],
                t["vintage"]["wine"]["seo_name"],
                t["vintage"]["statistics"]["ratings_average"],
                t["vintage"]["wine"]["region"]["country"]["name"],
                t["price"]["amount"],
                t["price"]["url"],
            )
            for t in r["explore_vintage"]["matches"]
        ]

        dataframe = pd.DataFrame(result_table, columns=["name", "seo", "rating", "country", "price", "url"])
        return dataframe

    def __generate_answer(self, df: pd.DataFrame, user_id):
        self.df = df[df["country"] == self.users[user_id].wine_country]
        self.df = df.sort_values(by="rating", ascending=False)
        self.df = df.drop_duplicates(subset="name", keep="first")

        if len(self.df) == 0:
            ans = WineBotVocabulary.FAIL.value
            self.users[user_id].checkpoint = 0

        else:
            if self.users[user_id].attempts < len(df):
                ans = (
                    f"Предлагаю попробовать {self.df.name.tolist()[self.users[user_id].attempts]}. На Vivino у него рейтинг "
                    f"{self.df.rating.tolist()[self.users[user_id].attempts]} – это самое лучшее, что я смог найти в "
                    f"данной ценовой категории. Заказать за {self.df.price.tolist()[self.users[user_id].attempts]} рублей и "
                    f"подробнее ознакомиться с характеристиками можно здесь: "
                    f"{self.df.url.tolist()[self.users[user_id].attempts]}.\n\nПо этому запросу вина еще будем смотреть?"
                )
                self.users[user_id].checkpoint += 1
        return ans

    def generate_one_more_answer(self, user_id):
        if self.users[user_id].attempts < len(self.df):
            self.users[user_id].attempts += 1
            question = random.choice(AvailableOption.GENERAL.value.api_short_code)
            introduction = random.choice(AvailableOption.GENERAL.value.user_name)
            ans = (
                f"{introduction} {self.df.name.tolist()[self.users[user_id].attempts]}. Рейтинг на Vivino: "
                f"{self.df.rating.tolist()[self.users[user_id].attempts]}. Если заказать на "
                f"{self.df.url.tolist()[self.users[user_id].attempts]}, будет стоить {self.df.price.tolist()[self.users[user_id].attempts]}. "
                f"\n\n{question}"
            )
            state = BOT_STATE.DASHA_DOMAIN

        else:
            quote = random.choice(self.quotes)
            ans = f"{AvailableOption.GENERAL.value.api_long_name} {quote} Надеюсь, был полезен!"
            state = BOT_STATE.DOMAIN_RECOGNITION
        return ans, state

    def generate_quote(self):
        quote = random.choice(self.quotes)
        ans = emoji.emojize(
            f"Отлично, надеюсь, был полезен! И, напоследок, твоя цитата дня: {quote} :red_heart:", variant="emoji_type"
        )
        return ans

    def get_result(self, user_id):
        r = self.__make_get_request(
            self.users[user_id].upper_price_bound,
            self.users[user_id].wine_type,
            self.users[user_id].attempts,
            self.users[user_id].country_code,
        )
        df = self.__filter_json_results(r)
        return self.__generate_answer(df, user_id)

    def generate_answer(self, msg: Union[List, str], user_id) -> Tuple[BOT_STATE, str]:
        if user_id not in self.users:
            self.users[user_id] = User()

        if isinstance(msg, str):
            msg = lemmatize(msg)

        if self.users[user_id].checkpoint == 0:
            self.users[user_id].checkpoint += 1
            return BOT_STATE.DASHA_DOMAIN, WineBotVocabulary.INTRO.value

        elif self.users[user_id].checkpoint == 1:
            types = lemmatize_list(AvailableOption.TYPES.value.user_name)
            for word in msg:
                if word in types:
                    self.users[user_id].wine_type = WineBotInterpreter.define_wine_type(msg)
                    self.users[user_id].checkpoint += 1
                    answer = WineBotVocabulary.QUESTION.value
                    break
                else:
                    answer = (
                        f"{WineBotVocabulary.ASK.value}"
                        f"{translate_list_to_str(AvailableOption.TYPES.value.user_name)} "
                    )

            return BOT_STATE.DASHA_DOMAIN, answer

        elif self.users[user_id].checkpoint == 2:
            countries = lemmatize_list(AvailableOption.COUNTRIES.value.user_name)
            for word in msg:
                if word in countries:
                    self.users[user_id].wine_country = WineBotInterpreter.define_wine_country(word)
                    self.users[user_id].country_code = WineBotInterpreter.define_wine_country(word, full_name=False)
                    self.users[user_id].checkpoint += 1
                    answer = WineBotVocabulary.PRICE.value
                    break
                else:
                    answer = (
                        f"{WineBotVocabulary.ASK.value}"
                        f"{translate_list_to_str(AvailableOption.COUNTRIES.value.api_code)}"
                    )
            return BOT_STATE.DASHA_DOMAIN, answer

        elif self.users[user_id].checkpoint == 3:
            if isinstance(msg, List):
                msg = msg[0]
            try:
                msg = int(msg)
                if msg > 0:
                    self.users[user_id].upper_price_bound = msg
                    answer = self.get_result(user_id)
                else:
                    answer = WineBotVocabulary.POSITIVE.value
            except ValueError:
                answer = WineBotVocabulary.NUMBER.value
            return BOT_STATE.DASHA_DOMAIN, answer

        elif self.users[user_id].checkpoint == 4:
            yes_ans = lemmatize_list(AvailableOption.AGREEMENT.value.user_name)
            no_ans = lemmatize_list(AvailableOption.AGREEMENT.value.api_code)
            for word in msg:
                if word in yes_ans:
                    answer, state = self.generate_one_more_answer(user_id)
                    break

                elif word in no_ans:
                    answer = self.generate_quote()
                    state = BOT_STATE.DOMAIN_RECOGNITION
                    self.users[user_id].checkpoint = 0
                    break

                else:
                    answer = BotVocabulary.ASK.value
                    state = BOT_STATE.DASHA_DOMAIN

            return state, answer
