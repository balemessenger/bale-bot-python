from balebot.models.messages.video_message import VideoMessage
from balebot.filters.filter import Filter


class VideoFilter(Filter):
    def match(self, message):
        if isinstance(message, VideoMessage):
            return self.validator(message) if self.validator else True
        else:
            return False
