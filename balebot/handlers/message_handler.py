from balebot.filters import DefaultFilter
from balebot.filters.filter import Filter
from balebot.handlers.handler import Handler
from balebot.models.base_models.fat_seq_update import FatSeqUpdate


class MessageHandler(Handler):
    def __init__(self, filters, callback):
        super(MessageHandler, self).__init__(callback=callback)

        if not filters:
            filters = DefaultFilter()

        if isinstance(filters, list) and all(
                isinstance(message_filter, Filter) for message_filter in filters):
            self.filters = filters
        elif isinstance(filters, Filter):
            self.filters = [filters]
        else:
            raise ValueError("filters don't have acceptable format.")

    def check_update(self, update):
        if isinstance(update, FatSeqUpdate) and update.is_message_update():
            message = update.get_effective_message()

            return any(message_filter.match(message) for message_filter in self.filters)

    def handle_update(self, dispatcher, update):
        return self.callback(dispatcher.bot, update)

    def is_default_handler(self):
        for message_filter in self.filters:
            if isinstance(message_filter, DefaultFilter):
                return True
