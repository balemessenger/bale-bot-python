from balebot.models.messages.contact_message import ContactMessage
from balebot.models.messages.json_message import JsonMessage
from balebot.filters.filter import Filter


class ContactFilter(Filter):
    def match(self, message):
        return isinstance(message, ContactMessage)
