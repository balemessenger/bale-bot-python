import json as json_handler

from balebot.models.constants.peer_type import PeerType
from .peer import Peer


class GroupPeer(Peer):
    def __init__(self, peer_id, access_hash):
        super(GroupPeer, self).__init__(peer_type=PeerType.group, peer_id=peer_id, access_hash=access_hash)

    @classmethod
    def load_from_json(cls, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError("json input has unacceptable format.")

        peer_type = json_dict.get('$type', None)
        peer_id = json_dict.get('id', None)
        access_hash = json_dict.get('accessHash', None)

        if (peer_type != PeerType.group) or (not peer_id) or (not access_hash):
            raise ValueError("peer_type , peer_id and access_hash should have correct values.")

        return cls(peer_id=peer_id, access_hash=access_hash)
