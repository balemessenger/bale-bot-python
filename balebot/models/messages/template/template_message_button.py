import json as json_handler


class TemplateMessageButton:
    def __init__(self, text, value, action):
        self.text = str(text)
        self.value = str(value)
        self.action = int(action)

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
