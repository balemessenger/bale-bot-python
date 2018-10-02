from balebot.filters.filter import Filter
from balebot.models.messages.location_message import LocationMessage


class LocationFilter(Filter):
    def match(self, message):
        return isinstance(message, LocationMessage)
