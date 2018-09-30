import json as json_handler

from balebot.models.base_models.response_body import ResponseBody
from balebot.models.constants.errors import Error


class MessageEdited(ResponseBody):
    def __init__(self, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)

        self.date = json_dict.get("date", None)
        self.seq = json_dict.get("seq", None)
