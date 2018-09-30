import json as json_handler

from balebot.models.base_models.peer import Peer
from balebot.models.base_models.request_body import RequestBody
from balebot.models.constants.errors import Error
from balebot.models.constants.request_type import RequestType
from balebot.models.messages.base_message import BaseMessage
from balebot.utils.util_functions import generate_random_id


class EditMessage(RequestBody):
    def __init__(self, updated_message, peer, random_id):
        if isinstance(updated_message, BaseMessage) and isinstance(peer, Peer):
            self.updated_message = updated_message
            self.peer = peer
            self._random_id = str(random_id)

        else:
            raise ValueError(Error.unacceptable_object_type)

    def get_json_object(self):

        data = {
            "$type": RequestType.edit_message,
            "peer": self.peer.get_json_object(),
            "randomId": self._random_id,
            "message": self.updated_message.get_json_object()
        }

        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())
