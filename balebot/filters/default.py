from balebot.filters.filter import Filter


class DefaultFilter(Filter):
    def match(self, message):
        return True
