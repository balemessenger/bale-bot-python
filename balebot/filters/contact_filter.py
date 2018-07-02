from balebot.models.base_models.contact import Contact
from balebot.models.messages.json_message import JsonMessage
from balebot.filters.filter import Filter


class ContactFilter(Filter):
    def match(self, message):
        if isinstance(message, JsonMessage):
            raw_json = message.raw_json
            return isinstance(raw_json, Contact)
        else:
            return False
