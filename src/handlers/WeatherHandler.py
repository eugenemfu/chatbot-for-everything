from src.handlers.handlers import StateHandler
from typing import Tuple
from definitions import BOT_STATE
import natasha
from util import lemmatize
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
            "сегодня",
            "завтра",
            "послезавтра",
            "понедельник",
            "вторник",
            "среда",
            "четверг",
            "пятница",
            "суббота",
            "воскресенье",
        ]

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
        return locations[0]

    def find_date(self, msg):
        dates = list(self.dates_extractor(msg))
        daywords = [_ for _ in lemmatize(msg) if _ in self.day_keywords]
        if len(dates) + len(daywords) != 1:
            return None
        elif len(dates) == 1:
            return msg[dates[0].start:dates[0].stop]
        elif len(daywords) == 1:
            return daywords[0]

    def get_forecast(self, city, date):
        return 'Погода в ' + city + ' ' + date

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
            return self.home_state, self.get_forecast(city, date)
        elif city is None and date is None:
            return self.additional_question_state, \
                'В каком городе и в какой день ты хочешь узнать погоду?'
        elif city:
            return self.additional_question_state, \
                f'В какой день тебя интересует погода в {city}?'
        elif date:
            return self.additional_question_state, \
                f'В каком городе тебя интересует погода {date}?'
