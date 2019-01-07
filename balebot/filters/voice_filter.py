from balebot.models.messages.voice_message import VoiceMessage
from balebot.filters.filter import Filter


class VoiceFilter(Filter):
    def __init__(self, validator=None):
        self.validator = validator if callable(validator) else None

    def match(self, message):
        if isinstance(message, VoiceMessage):
            return self.validator(message) if self.validator else True
        else:
            return False
