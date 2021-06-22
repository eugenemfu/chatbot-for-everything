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


class DashaHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.wine_type = None
        self.wine_country = None
        self.upper_price_bound = None
        self.country_code = None
        self.checkpoint = 0
        self.attempts = 0
        self.df = None
        self.quotes = list(pd.read_csv(Path(ROOT_DIR) / 'data/wine_quotes.csv')['quote'])

    def __make_get_request(self) -> dict:
        parameter_dict["price_range_max"] = self.upper_price_bound
        parameter_dict["wine_type_ids[]"] = self.wine_type
        parameter_dict["page"] = self.attempts
        parameter_dict["country_codes[]"] = self.country_code

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
        self.df = df[df["country"] == self.wine_country]
        self.df = df.sort_values(by='rating', ascending=False)
        self.df = df.drop_duplicates(subset='name', keep="first")

        if len(self.df) == 0:
            ans = WineBotVocabulary.FAIL.value
            self.checkpoint = 0

        else:
            if self.attempts < len(df):
                ans = f'Предлагаю попробовать {self.df.name.tolist()[self.attempts]}. На Vivino у него рейтинг ' \
                      f'{self.df.rating.tolist()[self.attempts]} – это самое лучшее, что я смог найти в ' \
                      f'данной ценовой категории. Заказать за {self.df.price.tolist()[self.attempts]} рублей и ' \
                      f'подробнее ознакомиться с характеристиками можно здесь: ' \
                      f'{self.df.url.tolist()[self.attempts]}.\n\nПо этому запросу вина еще будем смотреть?'
                self.checkpoint += 1
        return ans

    def generate_one_more_answer(self):
        if self.attempts < len(self.df):
            self.attempts += 1
            question = random.choice(AvailableOption.GENERAL.value.api_short_code)
            introduction = random.choice(AvailableOption.GENERAL.value.user_name)
            ans = f'{introduction} {self.df.name.tolist()[self.attempts]}. Рейтинг на Vivino: ' \
                  f'{self.df.rating.tolist()[self.attempts]}. Если заказать на ' \
                  f'{self.df.url.tolist()[self.attempts]}, будет стоить {self.df.price.tolist()[self.attempts]}. ' \
                  f'\n\n{question}'
            state = BOT_STATE.DASHA_DOMAIN

        else:
            quote = random.choice(self.quotes)
            ans = f'{AvailableOption.GENERAL.value.api_long_name} {quote} Надеюсь, был полезен!'
            state = BOT_STATE.DOMAIN_RECOGNITION
        return ans, state

    def generate_quote(self):
        quote = random.choice(self.quotes)
        ans = emoji.emojize(f'Отлично, надеюсь, был полезен! И, напоследок, твоя цитата дня: {quote} :red_heart:',
                            variant="emoji_type")
        return ans

    def get_result(self):
        r = self.__make_get_request()
        df = self.__filter_json_results(r)
        return self.__generate_answer(df)

    def generate_answer(self, msg: Union[List, str], user_id) -> Tuple[BOT_STATE, str]:
        if isinstance(msg, str):
            msg = lemmatize(msg)

        if self.checkpoint == 0:
            self.checkpoint += 1
            return BOT_STATE.DASHA_DOMAIN, WineBotVocabulary.INTRO.value

        elif self.checkpoint == 1:
            types = lemmatize_list(AvailableOption.TYPES.value.user_name)
            for word in msg:
                if word in types:
                    self.wine_type = WineBotInterpreter.define_wine_type(msg)
                    self.checkpoint += 1
                    answer = WineBotVocabulary.QUESTION.value
                    break
                else:
                    answer = f'{WineBotVocabulary.ASK.value}' \
                          f'{translate_list_to_str(AvailableOption.TYPES.value.user_name)} '

            return BOT_STATE.DASHA_DOMAIN, answer

        elif self.checkpoint == 2:
            countries = lemmatize_list(AvailableOption.COUNTRIES.value.user_name)
            for word in msg:
                if word in countries:
                    self.wine_country = WineBotInterpreter.define_wine_country(word)
                    self.country_code = WineBotInterpreter.define_wine_country(word, full_name=False)
                    self.checkpoint += 1
                    answer = WineBotVocabulary.PRICE.value
                    break
                else:
                    answer = f'{WineBotVocabulary.ASK.value}' \
                          f'{translate_list_to_str(AvailableOption.COUNTRIES.value.api_code)}'
            return BOT_STATE.DASHA_DOMAIN, answer

        elif self.checkpoint == 3:
            if isinstance(msg, List):
                msg = msg[0]
            try:
                msg = int(msg)
                if msg > 0:
                    self.upper_price_bound = msg
                    answer = self.get_result()
                else:
                    answer = WineBotVocabulary.POSITIVE.value
            except ValueError:
                answer = WineBotVocabulary.NUMBER.value
            return BOT_STATE.DASHA_DOMAIN, answer

        elif self.checkpoint == 4:
            yes_ans = lemmatize_list(AvailableOption.AGREEMENT.value.user_name)
            no_ans = lemmatize_list(AvailableOption.AGREEMENT.value.api_code)
            for word in msg:
                if word in yes_ans:
                    answer, state = self.generate_one_more_answer()
                    break

                elif word in no_ans:
                    answer = self.generate_quote()
                    state = BOT_STATE.DOMAIN_RECOGNITION
                    self.checkpoint = 0
                    break

                else:
                    answer = BotVocabulary.ASK.value
                    state = BOT_STATE.DASHA_DOMAIN

            return state, answer
