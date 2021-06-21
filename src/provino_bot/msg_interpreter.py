from src.provino_bot.vocabulary import WineType, WineCountry


class WineBotInterpreter(object):
    @staticmethod
    def define_wine_type(msg):
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
    def define_wine_country(word):
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
