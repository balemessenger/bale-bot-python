import json as json_handler

from balebot.models.base_models.jsonable import Jsonable
from balebot.models.constants.errors import Error


class GroupMember(Jsonable):
    def __init__(self, user_id, invite_user_id, member_since, is_admin=None):
        self.user_id = str(user_id)
        self.invite_user_id = str(invite_user_id)
        self.member_since = str(member_since)
        self.is_admin = bool(is_admin) if is_admin else None

    def get_json_object(self):
        data = {
            "userId": self.user_id,
            "inviteUserId": self.invite_user_id,
            "memberSince": self.member_since,
            "isAdmin": self.is_admin,
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

        user_id = json_dict.get('userId', None)
        invite_user_id = json_dict.get('inviteUserId', None)
        member_since = json_dict.get('memberSince', None)
        is_admin = json_dict.get('isAdmin', None)

        if (not user_id) or (not invite_user_id) or (member_since is None):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(user_id=user_id, invite_user_id=invite_user_id, member_since=member_since, is_admin=is_admin)
