from balebot.models.constants.update_body_type import UpdateBodyType

from balebot.models.server_updates import bot_read_update_body
from balebot.models.server_updates import message_update_body
from balebot.models.server_updates import raw_update_body
from balebot.models.server_updates import bot_received_update_body


class UpdateBodyFactory:
    @staticmethod
    def create_update_body(body_json_dict):
        update_body_type = body_json_dict.get("$type", None)

        if update_body_type == UpdateBodyType.message:
            return message_update_body.MessageUpdate(body_json_dict)

        elif update_body_type == UpdateBodyType.bot_read_update:
            return bot_read_update_body.BotReadUpdate(body_json_dict)

        elif update_body_type == UpdateBodyType.bot_received_update:
            return bot_received_update_body.BotReceivedUpdate(body_json_dict)

        elif update_body_type == UpdateBodyType.raw_update:
            return raw_update_body.RawUpdate(body_json_dict)
