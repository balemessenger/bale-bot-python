from balebot.models.constants.value_type import ValueType
from balebot.models.base_models.value_types import int32_val
from balebot.models.base_models.value_types import int64_val
from balebot.models.base_models.value_types import boolean_value
from balebot.models.base_models.value_types import double_val
from balebot.models.base_models.value_types import string_val
from balebot.models.base_models.value_types import array_val
from balebot.models.base_models.value_types import map_value


class RawValueFactory:
    @staticmethod
    def create_raw_value(json_dict):
        raw_value_type = json_dict.get("$type", None)

        if raw_value_type == ValueType.int32_val:
            return int32_val.Int32Val.load_from_json(json_dict)

        if raw_value_type == ValueType.int64_val:
            return int64_val.Int64Val.load_from_json(json_dict)

        elif raw_value_type == ValueType.boolean_value:
            return boolean_value.BooleanValue.load_from_json(json_dict)

        elif raw_value_type == ValueType.double_val:
            return double_val.DoubleVal.load_from_json(json_dict)

        elif raw_value_type == ValueType.string_val:
            return string_val.StringVal.load_from_json(json_dict)

        elif raw_value_type == ValueType.array_val:
            return array_val.ArrayVal.load_from_json(json_dict)

        elif raw_value_type == ValueType.map_value:
            return map_value.MapValue.load_from_json(json_dict)

    @staticmethod
    def get_value(raw_value):
        if isinstance(raw_value, int32_val.Int32Val):
            return raw_value.value

        if isinstance(raw_value, int64_val.Int64Val):
            return raw_value.value

        elif isinstance(raw_value, boolean_value.BooleanValue):
            return raw_value.value

        elif isinstance(raw_value, double_val.DoubleVal):
            return raw_value.value

        elif isinstance(raw_value, string_val.StringVal):
            return raw_value.text

        elif isinstance(raw_value, array_val.ArrayVal):
            return raw_value.values

        elif isinstance(raw_value, map_value.MapValue):
            return raw_value.items
