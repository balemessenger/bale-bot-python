import json as json_handler

from balebot.models.base_models.group_peer import GroupPeer
from balebot.models.base_models.user_peer import UserPeer

from balebot.models.base_models.request_body import RequestBody
from balebot.models.constants.request_type import RequestType


class InviteUser(RequestBody):
    def __init__(self, group_peer, user_peer):
        if isinstance(group_peer, GroupPeer):
            self.group_peer = group_peer

        if isinstance(user_peer, UserPeer):
            self.user_peer = user_peer

    def get_json_object(self):
        data = {
            "$type": RequestType.invite_user,
            "groupPeer": self.group_peer.get_json_object(),
            "userPeer": self.user_peer.get_json_object(),
        }

        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())
