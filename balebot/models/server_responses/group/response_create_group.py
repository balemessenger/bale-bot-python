import json as json_handler

from balebot.models.base_models.group_peer import GroupPeer
from balebot.models.constants.errors import Error

from balebot.models.base_models.response_body import ResponseBody


class ResponseCreateGroup(ResponseBody):
    def __init__(self, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)

        self.group_peer = GroupPeer.load_from_json(json_dict.get("peer", None))
