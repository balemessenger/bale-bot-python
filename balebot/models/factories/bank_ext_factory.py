from balebot.models.base_models.banking import deprecated_receipt
from balebot.models.base_models.banking import deprecated_receipt_message
from balebot.models.base_models.banking import receipt_message
from balebot.models.constants.bank_ext_types import BankExtTypes


class BankExtFactory:
    @staticmethod
    def create_bank_ext(json_dict):
        bank_ext_type = json_dict.get("$type", None)

        if bank_ext_type == BankExtTypes.deprecated_receipt_message:
            return deprecated_receipt_message.DeprecatedReceiptMessage.load_from_json(json_dict)

        elif bank_ext_type == BankExtTypes.deprecated_receipt:
            return deprecated_receipt.DeprecatedReceipt.load_from_json(json_dict)

        elif bank_ext_type == BankExtTypes.receipt_message:
            return receipt_message.ReceiptMessage.load_from_json(json_dict)

        else:
            return None
