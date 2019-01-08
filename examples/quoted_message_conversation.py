"""QuotedMessage conversation with bot."""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler, QuotedMessageHandler
from balebot.models.messages import *
from balebot.updater import Updater
from balebot.utils.logger import Logger

# Bale Bot Authorization Token
updater = Updater(token="PUT YOUR TOKEN HERE",
                  loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher
my_logger = Logger.get_logger()  # Create a logger and name it my_logger


def success_send_message(response, user_data):
    kwargs = user_data['kwargs']
    update = kwargs["update"]
    user_peer = update.get_effective_user()
    my_logger.info("Your message has been sent successfully.", extra={"user_id": user_peer.peer_id, "tag": "info"})


def failure_send_message(response, user_data):
    kwargs = user_data['kwargs']
    update = kwargs["update"]
    user_peer = update.get_effective_user()
    my_logger.error("Sending message has been failed", extra={"user_id": user_peer.peer_id, "tag": "error"})


@dispatcher.command_handler(["/start"])
def conversation_starter(bot, update):
    message = TextMessage("*Hi , nice to meet you*\nplease forward or reply message to me.")
    user_peer = update.get_effective_user()
    kwargs = {"message": message, "update": update}
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message,
                     kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update, [
        QuotedMessageHandler(DefaultFilter(), echo_quoted)
    ])


@dispatcher.quoted_message_handler(DefaultFilter())
def echo_quoted(bot, update):
    user_peer = update.get_effective_user()
    kwargs = {'update': update}
    quoted_sender_id = update.get_quoted_sender_peer_id()
    print("replied or forwarded message from peer_id: " + str(quoted_sender_id))
    output = update.get_quoted_message()
    bot.send_message(output, user_peer, success_callback=success_send_message, failure_callback=failure_send_message,
                     kwargs=kwargs)
    dispatcher.finish_conversation(update)


updater.run()
