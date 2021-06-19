from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

from definitions import TELEGRAM_TOKEN, BOT_STATE
from src.handlers.handlers import IntroHandler, DomainHandler, DashaHandler, KirillHandler, WeatherHandler


def main():
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    handlers = {
        BOT_STATE.INTRO.value: IntroHandler(),
        BOT_STATE.WEATHER.value: WeatherHandler(),
        BOT_STATE.KIRILL_DOMAIN.value: KirillHandler(),
        BOT_STATE.DASHA_DOMAIN.value: DashaHandler(),
    }
    domain_handler = DomainHandler(handlers)
    handlers[BOT_STATE.DOMAIN_RECOGNITION.value] = domain_handler

    states = {
        BOT_STATE.INTRO: [MessageHandler(Filters.text, handlers[BOT_STATE.INTRO.value])],
        BOT_STATE.DOMAIN_RECOGNITION: [MessageHandler(Filters.text, handlers[BOT_STATE.DOMAIN_RECOGNITION.value])],
        BOT_STATE.WEATHER: [MessageHandler(Filters.text, handlers[BOT_STATE.WEATHER.value])],
        BOT_STATE.KIRILL_DOMAIN: [MessageHandler(Filters.text, handlers[BOT_STATE.KIRILL_DOMAIN.value])],
        BOT_STATE.DASHA_DOMAIN: [MessageHandler(Filters.text, handlers[BOT_STATE.DASHA_DOMAIN.value])],
    }

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", handlers[BOT_STATE.INTRO.value])],
        states=states,
        fallbacks=[CommandHandler("start", handlers[BOT_STATE.INTRO.value])],
    )

    dispatcher.add_handler(conv_handler)

    print("Bot's started!")

    updater.start_polling()

    updater.idle()

    print("Quitting!")


if __name__ == "__main__":
    main()
