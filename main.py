#!/usr/bin/env python

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я еще ничего не умею, но скоро научусь. А пока почитай интересную статью: https://meduza.io/feature/2021/04/30/pochemu-meduzu-priznali-inostrannym-agentom-i-kto-za-etim-stoit-nam-poka-izvestny-dve-versii')
    return 0


def general(update: Update, context: CallbackContext):
    update.message.reply_text("Я не понимаю.")
    return 0


def main():
    updater = Updater("1753906220:AAFkY3dCToWvnVZIh_wvAub8jaG5eYi3FN8")

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            0: [MessageHandler(Filters.text, general)]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
