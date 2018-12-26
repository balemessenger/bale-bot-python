from balebot.models.messages.text_message import TextMessage
import re
from balebot.filters.filter import Filter


class TextFilter(Filter):
    def __init__(self, keywords=None, exact=None, pattern=None, validator=None, include_commands=True):
        self.keywords = []
        if isinstance(keywords, list):
            self.keywords += keywords
        elif isinstance(keywords, str):
            self.keywords.append(keywords)

        self.pattern = ('^'+str(exact)+'$') if exact else pattern
        self.validator = validator if callable(validator) else None
        self.include_commands = include_commands

    def match(self, message):
        if isinstance(message, TextMessage):
            text = message.text
            if not self.include_commands:
                if text.startswith("/"):
                    return False

            if not self.pattern and not self.keywords and not self.validator:
                return True

            if self.find_keywords(text):
                return True
            elif self.find_pattern(text):
                return True
            elif self.validate(text):
                return True
        else:
            return False

    def find_keywords(self, text):
        for keyword in self.keywords:
            if keyword:
                if text.find(keyword) != -1:
                    return True
        return False

    def find_pattern(self, text):
        if self.pattern:
            return re.search(self.pattern, text)
        else:
            return False

    def validate(self, text):
        if self.validator:
            return self.validator(text)
