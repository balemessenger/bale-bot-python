class Filter:
    def __init__(self, validator=None):
        self.validator = validator if callable(validator) else None

    def match(self, message):
        raise NotImplementedError

    def validate(self, obj):
        return self.validator(obj) if self.validator else False
