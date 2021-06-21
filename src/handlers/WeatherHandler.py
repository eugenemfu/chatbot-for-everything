import requests

from src.handlers.handlers import StateHandler
from typing import Tuple, Dict
from definitions import BOT_STATE

from geopy.geocoders import Nominatim


class WeatherHandler(StateHandler):
    def __init__(self, state_id: int = BOT_STATE.DOMAIN_RECOGNITION):
        super().__init__(state_id)
        self.ya_key = "90afa07e-a2d3-4af8-aa37-c8254e7848f6"
        self.ya_api = "https://api.weather.yandex.ru/v2/forecast?"

    def generate_answer(self, msg: str, user_id) -> Tuple[int, str]:
        ans = "asd"
        next_state = self.state_id
        r = self.__request("Омск")
        return next_state, ans

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
            "X-Yandex-API-Key": self.ya_key,
        }

        r = requests.get(self.ya_api,
                         params=params,
                         headers=header
                         )

        return r.json()
