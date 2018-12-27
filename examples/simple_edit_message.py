"""Simple Bot to edit Bale messages."""

import asyncio

from balebot.filters import DefaultFilter, TextFilter
from balebot.models.messages import TextMessage
from balebot.updater import Updater
from balebot.utils.logger import Logger

# Bale Bot Authorization Token

updater = Updater(token="TOKEN",
                  loop=asyncio.get_event_loop())
# Define dispatcher
dispatcher = updater.dispatcher
my_logger = Logger.get_logger()  # Create a logger and name it my_logger


# Both of success and failure functions are optional

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


request_random_id = None


@dispatcher.command_handler(commands='/start')
def start(bot, update):
    message = TextMessage('*Hello this message will be edited when you send /edit command*')
    # Send a message to client
    request = bot.respond(update, message, success_callback=success_send_message, failure_callback=failure_send_message)
    global request_random_id
    request_random_id = request.get_json_object()['body']['randomId']
    print(request_random_id)


@dispatcher.command_handler(commands='/edit')
def edit(bot, update):
    user_peer = update.get_effective_user()
    message = TextMessage('*message edited*')
    # edit nd a message to client
    bot.edit_message(message=message, user_peer=user_peer, random_id=request_random_id,
                     success_callback=success_send_message, failure_callback=failure_send_message)


# Run the bot!
updater.run()
