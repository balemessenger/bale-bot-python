import json as json_handler

from balebot.models.base_models.response_body import ResponseBody
from balebot.models.constants.errors import Error


class BotError(ResponseBody):
    def __init__(self, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)

        self.code = json_dict.get("code", None)
        self.tag = json_dict.get("tag", None)
        self.data = json_dict.get("data", None)
        self.retry_in = json_dict.get("retryIn", None)
