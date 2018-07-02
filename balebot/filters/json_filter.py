from balebot.models.messages.json_message import JsonMessage
from balebot.filters.filter import Filter


class JsonFilter(Filter):
    def match(self, message):
        return isinstance(message, JsonMessage)
