import requests

from src.handlers.handlers import StateHandler
from typing import Tuple, Dict
from definitions import BOT_STATE, WEATHER_API, WEATHER_TOKEN

from geopy.geocoders import Nominatim
import natasha
from util import lemmatize
import datetime
import time


class WeatherHandler(StateHandler):
    def __init__(self,
                 home_state: int = BOT_STATE.DOMAIN_RECOGNITION,
                 additional_question_state: int = BOT_STATE.WEATHER):
        self.home_state = home_state
        self.additional_question_state = additional_question_state
        self.city = dict()
        self.date = dict()
        self.morph_vocab = natasha.MorphVocab()
        self.dates_extractor = natasha.DatesExtractor(self.morph_vocab)
        self.segmenter = natasha.Segmenter()
        self.emb = natasha.NewsEmbedding()
        self.morph_tagger = natasha.NewsMorphTagger(self.emb)
        self.syntax_parser = natasha.NewsSyntaxParser(self.emb)
        self.ner_tagger = natasha.NewsNERTagger(self.emb)
        self.day_keywords = [
            "понедельник",
            "вторник",
            "среда",
            "четверг",
            "пятница",
            "суббота",
            "воскресенье",
            "сегодня",
            "завтра",
            "послезавтра",
        ]
        self.translate = {
            'clear': 'ясно',
            'partly-cloudy': 'малооблачно',
            'cloudy': 'облачно с прояснениями',
            'overcast': 'пасмурно',
            'drizzle': 'морось',
            'light-rain': 'небольшой дождь',
            'rain': 'дождь',
            'moderate-rain': 'умеренно сильный дождь',
            'heavy-rain': 'сильный дождь',
            'continuous-heavy-rain': 'длительный сильный дождь',
            'showers': 'ливень',
            'wet-snow': 'дождь со снегом',
            'light-snow': 'небольшой снег',
            'snow': 'снег',
            'snow-showers': 'снегопад',
            'hail': 'град',
            'thunderstorm': 'гроза',
            'thunderstorm-with-rain': 'дождь с грозой',
            'thunderstorm-with-hail': 'гроза с градом',
        }

    def find_city(self, msg):
        doc = natasha.Doc(msg.title())
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)
        doc.tag_ner(self.ner_tagger)
        if doc.spans is None:
            return None
        locations = [_.text for _ in doc.spans if _.type == natasha.LOC]
        if len(locations) != 1:
            return None
        return ' '.join(lemmatize(locations[0]))

    def find_date(self, msg):
        #dates = list(self.dates_extractor(msg))
        daywords = [_ for _ in lemmatize(msg) if _ in self.day_keywords]
        if len(daywords) != 1: # len(dates) + len(daywords) != 1:
            return None
        #elif len(dates) == 1:
        #    return msg[dates[0].start:dates[0].stop]
        elif len(daywords) == 1:
            return self.day_keywords.index(daywords[0])

    def __get_coords(self, city: str) -> Tuple[float, float]:
        geolocator = Nominatim(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0")
        location = geolocator.geocode(city)
        return location.latitude, location.longitude

    def __request(self, city: str) -> Dict:
        la, lo = self.__get_coords(city)
        params = {
            "lat": la,
            "lon": lo,
            "lang": "ru_RU"
        }
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "X-Yandex-API-Key": WEATHER_TOKEN,
        }

        r = requests.get(WEATHER_API,
                         params=params,
                         headers=header
                         )

        return r.json()

    def get_weather(self, city, date):
        forecast = self.__request(city)
        today = datetime.date.today()
        today_weekday = today.weekday()
        if date < 7:
            day = today + datetime.timedelta(days=(date-today_weekday)%7)
            day = day.strftime("%Y-%m-%d")
        else:
            day = today + datetime.timedelta(days=date-7)
            day = day.strftime("%Y-%m-%d")

        for fc in forecast['forecasts']:
            if fc['date'] != day:
                continue
            temp = str(fc['parts']['day_short']['temp'])
            condition = self.translate[fc['parts']['day_short']['condition']]

        return condition.title() + ', ' + temp + ' C'

    def generate_answer(self, msg, user_id) -> Tuple[int, str]:
        city = self.find_city(msg)
        date = self.find_date(msg)

        if city is None:
            if user_id in self.city:
                city = self.city[user_id]
        else:
            self.city[user_id] = city

        if date is None:
            if user_id in self.date:
                date = self.date[user_id]
        else:
            self.date[user_id] = date

        if city and date:
            self.date.pop(user_id)
            return self.home_state, self.get_weather(city, date)
        elif city is None and date is None:
            return self.additional_question_state, \
                'В каком городе и в какой день ты хочешь узнать погоду?'
        elif city:
            return self.additional_question_state, \
                f'В какой день тебя интересует погода?'
        elif date:
            return self.additional_question_state, \
                f'В каком городе тебя интересует погода?'
