from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

from definitions import TELEGRAM_TOKEN, BOT_STATE
from src.handlers.handlers import IntroHandler, DomainHandler, DashaHandler, KirillHandler, WeatherHandler


def main():
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    handlers = {
        BOT_STATE.INTRO: IntroHandler(),
        BOT_STATE.DOMAIN_RECOGNITION: DomainHandler(),
        BOT_STATE.WEATHER: WeatherHandler(),
        BOT_STATE.KIRILL_DOMAIN: KirillHandler(),
        BOT_STATE.DASHA_DOMAIN: DashaHandler(),
    }

    states = {
        BOT_STATE.INTRO: [MessageHandler(Filters.text, handlers[BOT_STATE.INTRO])],
        BOT_STATE.DOMAIN_RECOGNITION: [MessageHandler(Filters.text, handlers[BOT_STATE.DOMAIN_RECOGNITION])],
        BOT_STATE.WEATHER: [MessageHandler(Filters.text, handlers[BOT_STATE.WEATHER])],
        BOT_STATE.KIRILL_DOMAIN: [MessageHandler(Filters.text, handlers[BOT_STATE.KIRILL_DOMAIN])],
        BOT_STATE.DASHA_DOMAIN: [MessageHandler(Filters.text, handlers[BOT_STATE.DASHA_DOMAIN])],
    }

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", handlers[BOT_STATE.INTRO])],
        states=states,
        fallbacks=[CommandHandler("start", handlers[BOT_STATE.INTRO])],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
