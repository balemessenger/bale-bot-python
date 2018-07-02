import json as json_handler

from balebot.models.factories import message_factory
from balebot.models.messages.base_message import BaseMessage
from balebot.models.constants.message_type import MessageType
from balebot.models.constants.errors import Error


class PurchaseMessage(BaseMessage):
    def __init__(self, msg, account_number, amount, money_request_type):

        if isinstance(msg, BaseMessage):
            self.msg = msg
        else:
            raise ValueError(Error.unacceptable_object_type)

        self.account_number = str(account_number)

        if amount:
            self.amount = str(amount)
            self.regex_amount = "[" + str(amount) + "]"
        else:
            self.amount = "0"
            self.regex_amount = "[]"

        self.money_request_type = str(money_request_type)

    def get_json_object(self):
        data = {
            "$type": MessageType.purchase_message,
            "msg": self.msg.get_json_object(),
            "accountNumber": self.account_number,
            "amount": self.amount,
            "regexAmount": self.regex_amount,
            "moneyRequestType": {
                "$type": self.money_request_type
            }
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

        msg = message_factory.MessageFactory.create_message(json_dict.get('msg', None))
        account_number = json_dict.get('accountNumber', None)
        amount = json_dict.get('amount', None)

        if (msg is None) or (not account_number) or (amount is None):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(msg=msg, account_number=account_number, amount=amount)
