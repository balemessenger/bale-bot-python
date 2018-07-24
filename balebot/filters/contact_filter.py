from balebot.models.messages.contact_message import ContactMessage
from balebot.models.messages.json_message import JsonMessage
from balebot.filters.filter import Filter


class ContactFilter(Filter):
    def match(self, message):
        if isinstance(message, JsonMessage):
            raw_json = message.raw_json
            return isinstance(raw_json, ContactMessage)
        else:
            return False
