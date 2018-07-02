import json as json_handler

from balebot.models.constants.peer_type import PeerType
from balebot.models.constants.errors import Error

from .peer import Peer


class UserPeer(Peer):
    def __init__(self, peer_id, access_hash):
        super(UserPeer, self).__init__(peer_type=PeerType.user, peer_id=peer_id, access_hash=access_hash)

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

        if (peer_type != PeerType.user) or (not peer_id) or (not access_hash):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(peer_id=peer_id, access_hash=access_hash, )
