from balebot.models.messages.banking.bank_message import BankMessage
from balebot.filters.filter import Filter


class BankMessageFilter(Filter):
    def match(self, message):
        return isinstance(message, BankMessage)
