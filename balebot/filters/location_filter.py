from balebot.models.base_models.location import Location
from balebot.models.messages.json_message import JsonMessage
from balebot.filters.filter import Filter


class LocationFilter(Filter):
    def match(self, message):
        if isinstance(message, JsonMessage):
            raw_json = message.raw_json
            return isinstance(raw_json, Location)
        else:
            return False
