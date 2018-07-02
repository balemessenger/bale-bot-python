import json as json_handler

from balebot.models.constants.message_type import MessageType
from balebot.models.factories import bank_ext_factory
from balebot.models.messages.base_message import BaseMessage
from balebot.models.constants.errors import Error

from balebot.models.base_models.banking.bank_ext import BankExt


class BankMessage(BaseMessage):
    def __init__(self, bank_ext_message):

        if isinstance(bank_ext_message, BankExt):
            self.bank_ext_message = bank_ext_message
        else:
            raise ValueError(Error.unacceptable_object_type)

    def get_json_object(self):

        data = {
            "$type": MessageType.bank_message,
            "message": self.bank_ext_message.get_json_object(),
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

        bank_ext_message = bank_ext_factory.BankExtFactory.create_bank_ext(json_dict.get('message', None))

        if bank_ext_message is None:
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(bank_ext_message=bank_ext_message)
