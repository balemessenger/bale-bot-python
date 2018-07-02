import json as json_handler

from balebot.models.base_models.request_body import RequestBody
from balebot.models.constants.request_type import RequestType


class CreateGroup(RequestBody):
    def __init__(self, title):
        self.title = str(title)

    def get_json_object(self):
        data = {
            "$type": RequestType.create_group,
            "title": self.title,
        }

        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())
