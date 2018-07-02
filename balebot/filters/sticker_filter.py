from balebot.models.messages.sticker_message import StickerMessage
from balebot.filters.filter import Filter


class StickerFilter(Filter):
    def match(self, message):
        return isinstance(message, StickerMessage)
