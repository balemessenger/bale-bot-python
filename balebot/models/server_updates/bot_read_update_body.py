import json as json_handler

from balebot.models.base_models.peer import Peer
from balebot.models.constants.errors import Error

from balebot.models.server_updates.update_body import UpdateBody


class BotReadUpdate(UpdateBody):
    def __init__(self, json_dict):
        if isinstance(json_dict, dict):
            json_dict = json_dict
        elif isinstance(json_dict, str):
            json_dict = json_handler.loads(json_dict)
        else:
            raise ValueError(Error.unacceptable_json)

        self.peer = Peer.load_from_json(json_dict.get("peer", None))
        self.start_date = json_dict.get("startDate", None)
        self.read_date = json_dict.get("readDate", None)
