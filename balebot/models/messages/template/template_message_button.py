import json as json_handler


class TemplateMessageButton:
    # text: str
    # value: str
    # action: int

    def __init__(self, text, value=None, action=None):
        self.text = str(text)
        self.value = str(value or text)
        self.action = int(action or 0)

    def get_json_object(self):
        data = {
            "text": self.text,
            "value": self.value,
            "action": self.action,
        }
        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())

    @classmethod
    def load_from_json(cls, json):
        pass
