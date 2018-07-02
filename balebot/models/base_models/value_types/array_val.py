import json as json_handler

from balebot.models.base_models.value_types.raw_value import RawValue
from balebot.models.constants.errors import Error

from balebot.models.constants.value_type import ValueType
from balebot.models.factories import raw_value_factory


class ArrayVal(RawValue):
    def __init__(self, value):
        if all(isinstance(item, RawValue) for item in value):
            self.values = value
        else:
            raise ValueError(Error.unacceptable_object_type)

    def get_json_object(self):
        data = {
            "$type": ValueType.array_val,
            "value": [value.get_json_object() for value in self.values],

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

        temp_values = json_dict.get('value', None)
        items = [raw_value_factory.RawValueFactory.create_raw_value(value) for value in temp_values]

        return cls(items=items)
