import json as json_handler
from balebot.models.constants.errors import Error

from balebot.models.base_models.avatar import Avatar
from balebot.models.base_models.group_member import GroupMember

from balebot.models.base_models.jsonable import Jsonable


class Group(Jsonable):
    def __init__(self, group_id, access_hash, title, is_member, creator_user_id, members,
                 about=None, avatar=None):
        self.id = str(group_id)
        self.access_hash = str(access_hash)
        self.title = str(title)
        self.is_member = bool(is_member)
        self.creator_user_id = str(creator_user_id)

        if all(isinstance(member, GroupMember) for member in members):
            self.members = members
        else:
            raise ValueError(Error.unacceptable_object_type)

        self.about = str(about) if about else None

        if avatar:
            if isinstance(avatar, Avatar):
                self.avatar = avatar
            else:
                raise ValueError(Error.unacceptable_object_type)
        else:
            self.avatar = None

    def get_json_object(self):
        data = {
            "id": self.id,
            "accessHash": self.access_hash,
            "title": self.title,
            "isMember": self.is_member,
            "creatorUserId": self.creator_user_id,
            "members": self.members,
            "about": self.about,
            "avatar": self.avatar,
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

        group_id = json_dict.get('id', None)
        access_hash = json_dict.get('accessHash', None)
        title = json_dict.get('title', None)
        is_member = json_dict.get('isMember', None)
        creator_user_id = json_dict.get('creatorUserId', None)
        members = [GroupMember.load_from_json(member) for member in json_dict.get('members', None)]

        if (not group_id) or (not access_hash) or (title is None) or (is_member is None) or (
                not creator_user_id) or (members is None):
            raise ValueError(Error.none_or_invalid_attribute)

        about = json_dict.get('about', None)
        avatar = Avatar.load_from_json(json_dict.get('avatar', None)) if json_dict.get('avatar', None) else None

        return cls(group_id=group_id, access_hash=access_hash, is_member=is_member, creator_user_id=creator_user_id,
                   members=members, title=title, about=about, avatar=avatar)
