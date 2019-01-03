from balebot.models.messages.photo_message import PhotoMessage
from balebot.filters.filter import Filter


class PhotoFilter(Filter):
    def match(self, message):
        if isinstance(message, PhotoMessage):
            return self.validator(message) if self.validator else True
        else:
            return False
