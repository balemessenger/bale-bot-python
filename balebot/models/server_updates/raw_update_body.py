import json as json_handler

from balebot.models.server_updates.update_body import UpdateBody
from balebot.models.constants.errors import Error


class RawUpdate(UpdateBody):
    def __init__(self, json_dict):
        if isinstance(json_dict, dict):
            json_dict = json_dict
        elif isinstance(json_dict, str):
            json_dict = json_handler.loads(json_dict)
        else:
            raise ValueError(Error.unacceptable_json)

        self.data = json_dict.get("data", None)
