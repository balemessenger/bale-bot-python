import json as json_handler

from balebot.models.messages.base_message import BaseMessage
from balebot.models.constants.errors import Error

from balebot.models.constants.message_type import MessageType


class TextMessage(BaseMessage):
    def __init__(self, text):

        self.text = str(text) if text else ""

    def get_json_object(self):
        data = {
            "$type": MessageType.text_message,
            "text": self.text

        }
        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())

    @classmethod
    def load_from_json(cls, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)

        text = json_dict.get('text', None)
        if text is None:
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(text=text)
