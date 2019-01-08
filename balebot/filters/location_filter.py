from balebot.filters.filter import Filter
from balebot.models.messages.location_message import LocationMessage


class LocationFilter(Filter):
    def match(self, message):
        if isinstance(message, LocationMessage):
            return self.validator(message) if self.validator else True
        else:
            return False
