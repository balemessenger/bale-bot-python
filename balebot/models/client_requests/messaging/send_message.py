import json as json_handler

from balebot.models.base_models.bot_quoted_message import BotQuotedMessage
from balebot.models.base_models.peer import Peer
from balebot.models.base_models.request_body import RequestBody
from balebot.models.constants.errors import Error
from balebot.models.constants.request_type import RequestType
from balebot.models.messages.base_message import BaseMessage
from balebot.utils.util_functions import generate_random_id


class SendMessage(RequestBody):
    def __init__(self, message, receiver_user, quoted_message=None, random_id=None):

        if isinstance(message, BaseMessage) and (
                isinstance(receiver_user, Peer) or isinstance(receiver_user, str)) and (
                isinstance(quoted_message, BotQuotedMessage) or not quoted_message):

            self.message = message
            self.receiver_user = receiver_user
            self.quoted_message = quoted_message

            if random_id:
                self._random_id = str(random_id)
            else:
                self._random_id = str(generate_random_id())

        else:
            raise ValueError(Error.unacceptable_object_type)

    def get_json_object(self):

        data = {
            "$type": RequestType.send_message,
            "randomId": self._random_id,
            "message": self.message.get_json_object(),
            "quotedMessage": self.quoted_message.get_json_object() if self.quoted_message else None,
        }
        if isinstance(self.receiver_user, Peer):
            data["peer"] = self.receiver_user.get_json_object()
        else:
            data["nickName"] = self.receiver_user

        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())