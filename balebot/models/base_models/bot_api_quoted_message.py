import json as json_handler
from balebot.models.constants.errors import Error

from balebot.models.factories import message_factory


class BotApiQuotedMessage:
    def __init__(self, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)

        self.message_id = json_dict.get("messageId", None)
        self.public_group_id = json_dict.get("publicGroupId", None)
        self.sender_id = json_dict.get("senderId", None)
        self.messageDate = json_dict.get("messageDate", None)
        self.message = message_factory.MessageFactory.create_message(json_dict.get("message", None)) \
            if json_dict.get("message", None) else None
