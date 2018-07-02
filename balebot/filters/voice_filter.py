from balebot.models.messages.voice_message import VoiceMessage
from balebot.filters.filter import Filter


class VoiceFilter(Filter):
    def match(self, message):
        return isinstance(message, VoiceMessage)
