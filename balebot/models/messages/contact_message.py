import json as json_handler

from balebot.models.base_models.raw_json import RawJson
from balebot.models.messages.base_message import BaseMessage
from balebot.models.constants.errors import Error
from balebot.models.constants.raw_json_type import RawJsonType
from balebot.models.constants.message_type import MessageType


class ContactMessage(RawJson, BaseMessage):
    def __init__(self, name, emails, phones):
        self.name = str(name)

        if isinstance(emails, list):
            self.emails = [str(email) for email in emails]
        else:
            raise ValueError(Error.unacceptable_object_type)

        if isinstance(phones, list):
            self.phones = ["".join(str(phone).split(" ")) for phone in phones]
        else:
            raise ValueError(Error.unacceptable_object_type)

    def get_json_object(self):

        data = {
            "$type": MessageType.json_message,
            "rawJson": json_handler.dumps({
                "dataType": RawJsonType.contact,
                "data": {
                    RawJsonType.contact: {
                        "name": self.name,
                        "emails": self.emails,
                        "phones": self.phones
                    }
                }
            })
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

        data = json_dict.get('data', None)
        contact = data.get(RawJsonType.contact, None)
        name = contact.get('name', None)
        emails = contact.get('emails', None)
        phones = contact.get('phones', None)

        return cls(name=name, emails=emails, phones=phones)
