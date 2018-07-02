import json as json_handler
from balebot.models.constants.errors import Error

from balebot.models.base_models.jsonable import Jsonable


class BotCommand(Jsonable):
    def __init__(self, slash_command, description, loc_key="a"):
        self.slash_command = str(slash_command)
        self.description = str(description)
        self.loc_key = str(loc_key) if loc_key else None

    def get_json_object(self):
        data = {
            "slashCommand": self.slash_command,
            "description": self.description,
            "locKey": self.loc_key,

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

        slash_command = json_dict.get('slashCommand', None)
        description = json_dict.get('description', None)
        loc_key = json_dict.get('locKey', None)

        if (slash_command is None) or (description is None):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(slash_command=slash_command, description=description, loc_key=loc_key)
