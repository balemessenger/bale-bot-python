import json as json_handler

from balebot.models.base_models.banking.bank_ext import BankExt
from balebot.models.base_models.value_types.map_value import MapValue
from balebot.models.constants.bank_ext_types import BankExtTypes
from balebot.models.constants.errors import Error
from balebot.models.factories import message_factory
from balebot.models.messages.base_message import BaseMessage


class DeprecatedReceipt(BankExt):
    def __init__(self, receipt_type, transfer_info, original_message=None):
        self._receipt_type = receipt_type

        if isinstance(transfer_info, MapValue):
            self._transfer_info = transfer_info
        else:
            raise ValueError(Error.unacceptable_object_type)

        if original_message:
            if isinstance(original_message, BaseMessage):
                self._original_message = original_message
            else:
                raise ValueError(Error.unacceptable_object_type)
        else:
            self._original_message = None

    def get_json_object(self):
        data = {
            "$type": BankExtTypes.deprecated_receipt,
            "receiptType": {
                "$type": self._receipt_type,
            },
            "transferInfo": self._transfer_info.get_json_object(),
            "originalMessage": self._original_message.get_json_object() if self._original_message else None,

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

        receipt_type = json_dict.get('receiptType', None)["$type"]
        transfer_info = MapValue.load_from_json(json_dict.get('transferInfo', None))
        original_message = message_factory.MessageFactory.create_message(
            json_dict.get('originalMessage', None)) if json_dict.get(
            'originalMessage', None) else None

        if (not receipt_type) or (transfer_info is None):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(receipt_type=receipt_type, transfer_info=transfer_info, original_message=original_message)
