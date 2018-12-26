from balebot.models.messages.banking.bank_message import BankMessage
from balebot.filters.filter import Filter


class BankMessageFilter(Filter):
    def __init__(self, validator=None):
        self.validator = validator if callable(validator) else None

    def match(self, message):
        if isinstance(message, BankMessage):
            return self.validator(message) if self.validator else True
        else:
            return False
