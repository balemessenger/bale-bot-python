from balebot.models.messages.video_message import VideoMessage
from balebot.filters.filter import Filter


class VideoFilter(Filter):
    def __init__(self, validator=None):
        self.validator = validator if callable(validator) else None

    def match(self, message):
        if isinstance(message, VideoMessage):
            return self.validator(message) if self.validator else True
        else:
            return False
