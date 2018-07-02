class Handler:
    def __init__(self, callback):
        self.callback = callback

    def check_update(self, update):
        raise NotImplementedError

    def handle_update(self, dispatcher, update):
        raise NotImplementedError

    def is_default_handler(self):
        raise NotImplementedError
