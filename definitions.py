import os
from enum import Enum, unique

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TELEGRAM_TOKEN = "1886759359:AAEk68CWKWjJ_MOw7LnLIEwG4aO-nI71qSY"
CHGK_MODEL_PATH = "chgk/models/new_data_model/"


@unique
class BOT_STATE(Enum):
    INTRO = 0
    DOMAIN_RECOGNITION = 1
    WEATHER = 2
    KIRILL_DOMAIN = 3
    DASHA_DOMAIN = 4
