from balebot.models.messages.text_message import TextMessage
import re
from balebot.filters.filter import Filter


class TextFilter(Filter):
    def __init__(self, keywords=None, exact_keywords=None, pattern=None, validator=None, include_commands=True):
        super(TextFilter, self).__init__(validator)
        self.keywords = []
        self.exact_keywords = []
        if isinstance(keywords, list):
            self.keywords += keywords
        elif isinstance(keywords, str):
            self.keywords.append(keywords)
        if isinstance(exact_keywords, list):
            self.exact_keywords += exact_keywords
        elif isinstance(exact_keywords, str):
            self.exact_keywords.append(exact_keywords)

        self.pattern = pattern
        self.validator = validator if callable(validator) else None
        self.include_commands = include_commands

    def match(self, message):
        if isinstance(message, TextMessage):
            text = message.text
            if not self.include_commands and text.startswith("/"):
                return False
            if not self.pattern and not self.keywords and not self.validator and not self.exact_keywords:
                return True
            elif self.find_keywords(text):
                return True
            elif self.find_exact_keywords(text):
                return True
            elif self.find_pattern(text):
                return True
            elif self.validate(text):
                return True
        else:
            return False

    def find_keywords(self, text):
        for exact_keyword in self.keywords:
            if exact_keyword == text:
                return True
        return False

    def find_exact_keywords(self, text):
        for keyword in self.exact_keywords:
            if keyword == text:
                return True
        return False

    def find_pattern(self, text):
        if self.pattern:
            return re.search(self.pattern, text)
        return False
