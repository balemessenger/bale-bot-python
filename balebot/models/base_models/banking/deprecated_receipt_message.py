import json as json_handler

from balebot.models.base_models.banking.bank_ext import BankExt
from balebot.models.base_models.value_types.map_value import MapValue
from balebot.models.constants.bank_ext_types import BankExtTypes
from balebot.models.constants.errors import Error
from balebot.models.factories import message_factory
from balebot.models.messages.base_message import BaseMessage


class DeprecatedReceiptMessage(BankExt):
    def __init__(self, partial_receipt_type, partial_transfer_info, partial_original_message=None,
                 partial_original_message_rid=None):

        self._partial_receipt_type = str(partial_receipt_type)

        if isinstance(partial_transfer_info, MapValue):
            self._partial_transfer_info = partial_transfer_info
        else:
            raise ValueError(Error.unacceptable_object_type)

        if partial_original_message:
            if isinstance(partial_original_message, BaseMessage):
                self._partial_original_message = partial_original_message
            else:
                raise ValueError(Error.unacceptable_object_type)
        else:
            self._partial_original_message = None

        self._partial_original_message_rid = str(partial_original_message_rid) if partial_original_message_rid else None

    def get_json_object(self):
        data = {
            "$type": BankExtTypes.deprecated_receipt_message,
            "partialReceiptType": {
                "$type": self._partial_receipt_type,
            },
            "partialTransferInfo": self._partial_transfer_info.get_json_object(),
            "partialOriginalMessage": self._partial_original_message.get_json_object() if self._partial_original_message
            else None,
            "partialOrginalMessageRID": self._partial_original_message_rid if self._partial_original_message else None,

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

        partial_receipt_type = json_dict.get('partial_receipt_type', None)["$type"]
        partial_transfer_info = MapValue.load_from_json(json_dict.get('partial_transfer_info', None))
        partial_original_message = message_factory.MessageFactory.create_message(
            json_dict.get('partial_original_message', None)) if json_dict.get(
            'partial_original_message', None) else None
        partial_original_message_rid = json_dict.get('partial_original_message_rid', None)

        if (not partial_receipt_type) or (partial_transfer_info is None):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(partial_receipt_type=partial_receipt_type,
                   partial_transfer_info=partial_transfer_info,
                   partial_original_message=partial_original_message,
                   partial_original_message_rid=partial_original_message_rid)
