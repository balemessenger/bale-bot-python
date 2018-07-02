import json as json_handler
import traceback
from importlib import import_module
from balebot.models.constants.errors import Error
from balebot.utils.logger import Logger

from balebot.models.server_responses.bot_error_response import BotError
from balebot.models.server_responses.bot_success_response import BotSuccess


class Response:
    def __init__(self, json):
        self.logger = Logger.get_logger()

        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)

        self._id = json_dict.get("id", None)
        self.body_json = json_dict.get("body", None)

        if self.body_json.get("tag", None):
            self.body = BotError(self.body_json)
            del self.body_json
        else:
            self.body = None

    def is_bot_error(self):
        return isinstance(self.body, BotError)

    def create_body(self, body_module_name, body_class_name):
        try:
            if self.body is None:
                if self.body_json.get("tag", None):
                    self.body = BotError(self.body_json)
                elif not self.body_json:
                    self.body = BotSuccess()
                else:
                    module_obj = import_module(body_module_name)
                    body_class = getattr(module_obj, body_class_name)
                    self.body = body_class(self.body_json)
                del self.body_json

        except Exception as ex:
            self.logger.error(ex, extra={"tag": "err"})
            traceback.print_exc()

    @property
    def id(self):
        return self._id
