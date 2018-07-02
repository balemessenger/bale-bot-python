from balebot.models.messages.video_message import VideoMessage
from balebot.filters.filter import Filter


class VideoFilter(Filter):
    def match(self, message):
        return isinstance(message, VideoMessage)
