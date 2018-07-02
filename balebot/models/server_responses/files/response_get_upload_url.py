import json as json_handler

from balebot.models.base_models.request_body import RequestBody
from balebot.models.constants.errors import Error


class ResponseGetUploadUrl(RequestBody):
    def __init__(self, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)

        self.file_id = json_dict.get("fileId", None)
        self.user_id = json_dict.get("userId", None)
        self.url = json_dict.get("url", None)
        self.dup = json_dict.get("dup", None)
