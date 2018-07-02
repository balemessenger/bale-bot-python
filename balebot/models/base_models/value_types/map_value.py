import json as json_handler

from balebot.models.base_models.value_types.map_value_item import MapValueItem
from balebot.models.constants.errors import Error

from balebot.models.base_models.value_types.raw_value import RawValue


class MapValue(RawValue):
    def __init__(self, items):

        if isinstance(items, dict) and all(isinstance(value, RawValue) for key, value in items):

            items_list = []
            for key, value in items:
                temp_dict = {
                    "key": str(key),
                    "value": value,
                }
                items_list.append(MapValueItem.load_from_json(temp_dict))

            self.items = items_list

        elif all(isinstance(item, MapValueItem) for item in items):

            self.items = items
        else:
            raise ValueError(Error.unacceptable_object_type)

    def get_json_object(self):

        data = {
            "$type": "MapValue",
            "items": [item.get_json_object() for item in self.items],

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

        temp_items = json_dict.get('items', None)
        items = [MapValueItem.load_from_json(item) for item in temp_items]

        return cls(items=items)

    def find_value(self, key):
        for item in self.items:
            if item.key == key:
                return item.value
        return
