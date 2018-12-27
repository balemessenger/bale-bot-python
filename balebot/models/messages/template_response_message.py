import json as json_handler

from balebot.models.messages.base_message import BaseMessage
from balebot.models.constants.errors import Error

from balebot.models.constants.message_type import MessageType


class TemplateResponseMessage(BaseMessage):
    def __init__(self, text, template_message_response_id):
        self.text = str(text)
        self.text_message = str(text)
        self.template_message_response_id = str(template_message_response_id)

    def get_json_object(self):
        data = {
            "$type": MessageType.template_response_message,
            "textMessage": self.text,
            "templateMessageResponseId": self.template_message_response_id,
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

        text = json_dict.get("textMessage", None)
        template_message_response_id = json_dict.get("templateMessageResponseId", None)

        if (text is None) or (template_message_response_id is None):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(text=text, template_message_response_id=template_message_response_id)
