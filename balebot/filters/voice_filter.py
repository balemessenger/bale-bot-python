from balebot.models.messages.voice_message import VoiceMessage
from balebot.filters.filter import Filter


class VoiceFilter(Filter):
    def match(self, message):
        if isinstance(message, VoiceMessage):
            return self.validator(message) if self.validator else True
        else:
            return False
