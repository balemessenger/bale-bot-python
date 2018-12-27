"""Bank message conversation with bot
"""
import asyncio

from balebot.filters import *
from balebot.filters.bank_message_filter import BankMessageFilter
from balebot.handlers import MessageHandler
from balebot.models.messages import *
from balebot.models.messages.banking.money_request_type import MoneyRequestType
from balebot.updater import Updater

# Bale Bot Authorization Token
updater = Updater(token="TOKEN",
                  loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher


def success(response, user_data):
    print("success : ", response)
    print(user_data)


def failure(response, user_data):
    print("failure : ", response)
    print(user_data)


@dispatcher.command_handler(["/start"])
def conversation_starter(bot, update):
    message = TextMessage("Hi , nice to meet you :)\nplease send me a photo")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(PhotoFilter(), purchase_message))


@dispatcher.message_handler(PhotoFilter())
def purchase_message(bot, update):
    message = update.get_effective_message()
    user_peer = update.get_effective_user()
    first_purchase_message = PurchaseMessage(msg=message, account_number=6037991067471130, amount=100,
                                             money_request_type=MoneyRequestType.normal)
    bot.send_message(first_purchase_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(BankMessageFilter(), payment),
                                                                MessageHandler(DefaultFilter(), default_handler)])


def payment(bot, update):
    message = update.get_effective_message()
    print("message:", message)
    success_payment = TextMessage("Thanks, your payment was successful")
    bot.reply(update, success_payment, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


def default_handler(bot, update):
    success_payment = TextMessage("Ops, something goes wrong")
    bot.reply(update, success_payment, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


updater.run()
