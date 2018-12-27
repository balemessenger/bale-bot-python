#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to Reply to Bale messages."""

from balebot.filters import DefaultFilter
from balebot.handlers import CommandHandler, MessageHandler
from balebot.updater import Updater


def start(bot, update):
    bot.reply(update, 'Hi!')


def help(bot, update):
    bot.reply(update, 'Help!')


def echo(bot, update):
    message = update.get_effective_message()
    bot.reply(update, message)


def main():
    # Bale Bot Authorization Token
    updater = Updater("TOKEN")

    # Define dispatcher
    dp = updater.dispatcher

    # Add Command Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Add Message Handlers
    dp.add_handler(MessageHandler(DefaultFilter(), echo))

    # Run the bot!
    updater.run()


if __name__ == '__main__':
    main()
