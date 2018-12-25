from balebot.models.messages.photo_message import PhotoMessage
from balebot.filters.filter import Filter


class PhotoFilter(Filter):
    def __init__(self, validator=None):
        self.validator = validator if isinstance(validator, function) else None

    def match(self, message):
        if isinstance(message, PhotoMessage):
            return self.validator(message) if self.validator else True
        else:
            return False
