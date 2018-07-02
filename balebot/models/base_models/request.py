import json as json_handler

from balebot.models.base_models.request_body import RequestBody
from balebot.models.constants.errors import Error

from balebot.models.base_models.jsonable import Jsonable


class Request(Jsonable):
    id_counter = 0

    def __init__(self, service, body):
        self._id = str(Request.id_counter)
        self.service = str(service)
        if isinstance(body, RequestBody):
            self.body = body
        else:
            raise ValueError(Error.unacceptable_object_type)

        Request.id_counter += 1

    def get_json_object(self):
        data = {
            "$type": "Request",
            "id": self._id,
            "service": self.service,
            "body": self.body.get_json_object(),
        }
        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())

    @classmethod
    def load_from_json(cls, json):
        pass

    @property
    def id(self):
        return self._id
