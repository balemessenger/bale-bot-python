
from balebot.models.base_models.jsonable import Jsonable


class RequestBody(Jsonable):
    @classmethod
    def load_from_json(cls, json):
        pass
