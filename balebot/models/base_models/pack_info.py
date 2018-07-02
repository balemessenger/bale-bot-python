import json as json_handler

from balebot.models.base_models.jsonable import Jsonable
from balebot.models.constants.errors import Error


class PackInfo(Jsonable):
    def __init__(self, pack_id, name):
        self.pack_id = str(pack_id)
        self.name = str(name)

    def get_json_object(self):
        data = {
            "id": self.pack_id,
            "name": self.name,
        }
        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())

    @classmethod
    def load_from_json(cls, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)

        pack_id = json_dict.get('id', None)
        name = json_dict.get('name', None)

        if (not pack_id) or (name is None):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(pack_id=pack_id, name=name)
