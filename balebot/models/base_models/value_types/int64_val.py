import json as json_handler

from balebot.models.base_models.value_types.raw_value import RawValue
from balebot.models.constants.errors import Error

from balebot.models.constants.value_type import ValueType


class Int64Val(RawValue):
    def __init__(self, value):
        self.value = str(value)

    def get_json_object(self):
        data = {
            "$type": ValueType.int64_val,
            "value": self.value,

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

        value = json_dict.get('value', None)

        return cls(value=value)
