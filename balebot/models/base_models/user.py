import json as json_handler

from balebot.models.base_models.avatar import Avatar
from balebot.models.base_models.bot_command import BotCommand
from balebot.models.base_models.contact_record import ContactRecord
from balebot.models.constants.errors import Error

from balebot.models.base_models.jsonable import Jsonable


class User(Jsonable):
    def __init__(self, user_id, access_hash, name, contact_records, preferred_languages, bot_commands,
                 sex=None, about=None, avatar=None, username=None, is_bot=None, time_zone=None):
        self.id = str(user_id)
        self.access_hash = str(access_hash)
        self.name = str(name)

        if all(isinstance(contact_record, ContactRecord) for contact_record in contact_records):
            self.contact_records = [ContactRecord(contact_record) for contact_record in contact_records]
        else:
            ValueError(Error.unacceptable_object_type)

        self.preferred_languages = list(preferred_languages)

        if all(isinstance(bot_command, BotCommand) for bot_command in bot_commands):
            self.bot_commands = bot_commands
        else:
            ValueError(Error.unacceptable_object_type)

        self.sex = int(sex) if sex else None
        self.about = str(about) if about else None

        if avatar:
            if isinstance(avatar, Avatar):
                self.avatar = avatar
            else:
                raise ValueError(Error.unacceptable_object_type)
        else:
            self.avatar = None

        self.username = str(username) if username else None
        self.is_bot = bool(is_bot) if is_bot else None
        self.time_zone = str(time_zone) if time_zone else None

    def get_json_object(self):

        data = {
            "id": self.id,
            "accessHash": self.access_hash,
            "name": self.name,
            "contactRecords": self.contact_records,
            "preferredLanguages": self.preferred_languages,
            "botCommands": self.bot_commands,
            "sex": self.sex,
            "about": self.about,
            "avatar": self.avatar,
            "username": self.username,
            "isBot": self.is_bot,
            "timeZone": self.time_zone,

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

        user_id = json_dict.get('id', None)
        access_hash = json_dict.get('accessHash', None)
        name = json_dict.get('name', None)
        contact_records = [ContactRecord(contact_record) for contact_record in json_dict.get('contactRecords', None)]
        preferred_languages = list(json_dict.get('preferredLanguages', None))
        bot_commands = [BotCommand.load_from_json(bot_command) for bot_command in json_dict.get('botCommands', None)]

        if (not user_id) or (not access_hash) or (name is None) or (contact_records is None) or (
                    preferred_languages is None) or (bot_commands is None):
            raise ValueError(Error.none_or_invalid_attribute)

        sex = json_dict.get('sex', None)
        about = json_dict.get('about', None)
        avatar = Avatar.load_from_json(json_dict.get('avatar', None)) if json_dict.get('avatar', None) else None
        username = json_dict.get('username', None)
        is_bot = json_dict.get('is_bot', None)
        time_zone = json_dict.get('timeZone', None)

        return cls(user_id=user_id, access_hash=access_hash, contact_records=contact_records,
                   preferred_languages=preferred_languages, bot_commands=bot_commands, name=name, sex=sex,
                   about=about, avatar=avatar, username=username, is_bot=is_bot, time_zone=time_zone)
