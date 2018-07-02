from balebot.models.messages.photo_message import PhotoMessage
from balebot.filters.filter import Filter


class PhotoFilter(Filter):
    def match(self, message):
        return isinstance(message, PhotoMessage)
