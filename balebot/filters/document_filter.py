from balebot.filters.filter import Filter
from balebot.models.messages.document_message import DocumentMessage


class DocumentFilter(Filter):
    def match(self, message):
        return isinstance(message, DocumentMessage) and DocumentMessage.is_raw_document_message(
            message.get_json_object())
