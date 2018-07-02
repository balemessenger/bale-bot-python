import json as json_handler
from balebot.models.constants.errors import Error


class ContactRecord:
    def __init__(self, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)

        self.type = json_dict.get("$type", None)

        if self.type == "Email":
            self.email = json_dict.get("email", None)

        elif self.type == "Phone":
            self.phone = json_dict.get("phone", None)
