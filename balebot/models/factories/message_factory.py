from balebot.models.constants.message_type import MessageType
from balebot.models.messages.banking import bank_message
from balebot.models.messages.banking import purchase_message
from balebot.models.messages import document_message
from balebot.models.messages import photo_message
from balebot.models.messages import sticker_message
from balebot.models.messages.template import template_message
from balebot.models.messages import text_message
from balebot.models.messages import unsupported_message
from balebot.models.messages import json_message
from balebot.models.messages import video_message
from balebot.models.messages import voice_message
from balebot.models.messages import template_response_message


class MessageFactory:
    @staticmethod
    def create_message(json_dict):
        message_type = json_dict.get("$type", None)

        if message_type == MessageType.text_message:
            return text_message.TextMessage.load_from_json(json_dict)

        elif message_type == MessageType.template_message:
            return template_message.TemplateMessage.load_from_json(json_dict)

        elif message_type == MessageType.purchase_message:
            return purchase_message.PurchaseMessage.load_from_json(json_dict)

        elif message_type == MessageType.unsupported_message:
            return unsupported_message.UnsupportedMessage.load_from_json(json_dict)

        elif message_type == MessageType.sticker_message:
            return sticker_message.StickerMessage.load_from_json(json_dict)

        elif message_type == MessageType.json_message:
            return json_message.JsonMessage.load_from_json(json_dict)

        elif message_type == MessageType.template_response_message:
            return template_response_message.TemplateResponseMessage.load_from_json(json_dict)

        elif message_type == MessageType.bank_message:
            return bank_message.BankMessage.load_from_json(json_dict)

        elif message_type == MessageType.document_message:

            if document_message.DocumentMessage.is_raw_document_message(json_dict):
                return document_message.DocumentMessage.load_from_json(json_dict)

            elif document_message.DocumentMessage.is_photo_message(json_dict):
                return photo_message.PhotoMessage.load_from_json(json_dict)

            elif document_message.DocumentMessage.is_video_message(json_dict):
                return video_message.VideoMessage.load_from_json(json_dict)

            elif document_message.DocumentMessage.is_voice_message(json_dict):
                return voice_message.VoiceMessage.load_from_json(json_dict)

        else:
            return None
