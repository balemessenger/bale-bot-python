import json as json_handler

from balebot.models.base_models.value_types.raw_value import RawValue
from balebot.models.constants.errors import Error

from balebot.models.factories import raw_value_factory


class MapValueItem:
    def __init__(self, key, value):
        if isinstance(value, RawValue):
            self.value = value
        else:
            raise ValueError(Error.unacceptable_object_type)
        self.key = str(key)

    def get_json_object(self):

        data = {
            "key": self.key,
            "value": self.value.get_json_object(),
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

        key = json_dict.get('key', None)

        tmp_value = json_dict.get('value', None)
        value = raw_value_factory.RawValueFactory.create_raw_value(tmp_value)

        if (key is None) or (value is None):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(key=key, value=value)
