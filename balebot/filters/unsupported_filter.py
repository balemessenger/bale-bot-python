from balebot.models.messages.unsupported_message import UnsupportedMessage
from balebot.filters.filter import Filter


class UnsupportedFilter(Filter):
    def match(self, message):
        return isinstance(message, UnsupportedMessage)
