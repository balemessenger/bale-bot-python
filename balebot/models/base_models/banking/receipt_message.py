import json as json_handler

from balebot.models.base_models.banking.bank_ext import BankExt
from balebot.models.base_models.value_types.map_value import MapValue
from balebot.models.constants.bank_ext_types import BankExtTypes
from balebot.models.constants.errors import Error


class ReceiptMessage(BankExt):
    def __init__(self, message, transfer_info):

        if isinstance(message, MapValue):
            self.message = message
        else:
            raise ValueError(Error.unacceptable_object_type)

        if isinstance(transfer_info, MapValue):
            self.transfer_info = transfer_info
        else:
            raise ValueError(Error.unacceptable_object_type)

    def get_json_object(self):
        data = {
            "$type": BankExtTypes.deprecated_receipt,
            "message": self.message.get_json_object(),
            "transferInfo": self.transfer_info.get_json_object(),
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

        message = MapValue.load_from_json(json_dict.get('message', None))
        transfer_info = MapValue.load_from_json(json_dict.get('transferInfo', None))

        if (message is None) or (transfer_info is None):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(message=message, transfer_info=transfer_info)
