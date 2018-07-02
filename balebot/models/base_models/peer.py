import json as json_handler

from balebot.models.base_models.jsonable import Jsonable
from balebot.models.constants.errors import Error


class Peer(Jsonable):
    def __init__(self, peer_type, peer_id, access_hash):
        self.type = str(peer_type)
        self.peer_id = str(peer_id)
        self.access_hash = str(access_hash)

    def get_json_object(self):
        data = {
            "$type": self.type,
            "id": self.peer_id,
            "accessHash": self.access_hash,
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

        peer_type = json_dict.get('$type', None)
        peer_id = json_dict.get('id', None)
        access_hash = json_dict.get('accessHash', None)

        if (not peer_type) or (not peer_id) or (not access_hash):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(peer_type=peer_type, peer_id=peer_id, access_hash=access_hash)
