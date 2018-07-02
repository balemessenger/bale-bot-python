import json as json_handler

from balebot.models.base_models.peer import Peer
from balebot.models.base_models.user_peer import UserPeer
from balebot.models.factories import message_factory
from balebot.models.server_updates.update_body import UpdateBody
from balebot.models.constants.errors import Error

from balebot.models.base_models.bot_api_quoted_message import BotApiQuotedMessage


class MessageUpdate(UpdateBody):
    def __init__(self, json_dict):
        if isinstance(json_dict, dict):
            json_dict = json_dict
        elif isinstance(json_dict, str):
            json_dict = json_handler.loads(json_dict)
        else:
            raise ValueError(Error.unacceptable_json)

        self.peer = Peer.load_from_json(json_dict.get("peer", None))
        self.sender_user = UserPeer.load_from_json(json_dict.get("sender", None))
        self.date = json_dict.get("date", None)
        self.random_id = json_dict.get("randomId", None)
        self.message = message_factory.MessageFactory.create_message(json_dict.get("message", None))
        self.quoted_message = BotApiQuotedMessage(json_dict.get("quotedMessage", None)) if json_dict.get(
            "quotedMessage", None) else None
