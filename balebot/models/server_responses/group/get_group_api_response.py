import json as json_handler

from balebot.models.base_models.avatar import Avatar
from balebot.models.base_models.response_body import ResponseBody
from balebot.models.base_models.value_types.map_value import MapValue
from balebot.models.constants.errors import Error

from balebot.models.base_models.member import Member


class GetGroupApiResponse(ResponseBody):
    def __init__(self, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)

        self.id = json_dict.get("id", None)
        self.access_hash = json_dict.get("accessHash", None)
        self.title = json_dict.get("title", None)

        self.avatar = Avatar.load_from_json(json_dict.get("avatar", None)) if json_dict.get("avatar", None) else None

        self.is_member = json_dict.get("isMember", None)
        self.creator_user_id = json_dict.get("creatorUserId", None)

        self.members = [Member.load_from_json(member) for member in json_dict.get("members", None)] if json_dict.get(
            "members", None) else None

        self.create_date = json_dict.get("createDate", None)
        self.is_admin = json_dict.get("isAdmin", None)
        self.theme = json_dict.get("theme", None)
        self.about = json_dict.get("about", None)
        self.is_hidden = json_dict.get("isHidden", None)
        self.ext = MapValue.load_from_json(json_dict.get("ext", None)) if json_dict.get("ext", None) else None
        self.members_count = json_dict.get("membersCount", None)
        self.group_type = json_dict.get("groupType", None)["$type"]
        self.can_send_message = json_dict.get("canSendMessage", None)
        self.nick = json_dict.get("nick", None)
        self.became_orphaned = json_dict.get("becameOrphaned", None)
        self.state_version = json_dict.get("stateVersion", None)
