from balebot.models.messages.template.template_message import TemplateMessage
from balebot.filters.filter import Filter


class TemplateMessageFilter(Filter):
    def match(self, message):
        return isinstance(message, TemplateMessage)
