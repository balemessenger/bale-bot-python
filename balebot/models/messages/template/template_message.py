import json as json_handler

from balebot.models.constants.message_type import MessageType
from balebot.models.messages.base_message import BaseMessage
from balebot.models.constants.errors import Error

from balebot.models.messages.template.template_message_button import TemplateMessageButton


class TemplateMessage(BaseMessage):
    message_id_counter = 0

    def __init__(self, general_message, btn_list):

        if isinstance(general_message, BaseMessage):
            self.general_message = general_message
        else:
            raise ValueError(Error.unacceptable_object_type)

        if isinstance(btn_list, list) and all(isinstance(btn, TemplateMessageButton) for btn in btn_list):
            self.btn_list = btn_list
        elif btn_list is None:
            self.btn_list = []
        else:
            raise ValueError(Error.unacceptable_object_type)

        self.template_message_id = str(TemplateMessage.message_id_counter)
        TemplateMessage.message_id_counter += 1

    def get_json_object(self):
        data = {
            "$type": MessageType.template_message,
            "generalMessage": self.general_message.get_json_object(),
            "templateMessageId": self.template_message_id,
            "btnList": [btn.get_json_object() for btn in self.btn_list],

        }
        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())

    def add_button(self, btn):
        if isinstance(btn, TemplateMessageButton):
            self.btn_list.append(btn)
        else:
            raise ValueError(Error.unacceptable_object_type)

    @classmethod
    def load_from_json(cls, json):
        pass
