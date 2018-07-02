import json as json_handler
from balebot.models.constants.errors import Error

from balebot.models.base_models.peer import Peer
from balebot.models.base_models.jsonable import Jsonable


class BotQuotedMessage(Jsonable):
    def __init__(self, message_id=None, peer=None):

        self.message_id = str(message_id) if message_id else None

        if peer:
            if isinstance(peer, Peer):
                self.peer = peer
            else:
                raise ValueError(Error.unacceptable_object_type)
        else:
            self.peer = None

    def get_json_object(self):
        data = {
            "messageId": self.message_id,
            "peer": self.peer.get_json_object() if self.peer else None,
        }

        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())

    @classmethod
    def load_from_json(cls, json):
        pass
