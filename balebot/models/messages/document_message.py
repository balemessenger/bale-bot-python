import json as json_handler

from balebot.models.constants.document_type import DocumentType
from balebot.models.constants.message_type import MessageType
from balebot.models.messages.base_message import BaseMessage
from balebot.models.constants.errors import Error

from balebot.models.messages.text_message import TextMessage


class DocumentMessage(BaseMessage):
    def __init__(self, file_id, access_hash, name, file_size, mime_type, caption_text=None,
                 checksum=None, algorithm=None, file_storage_version=1):
        self.file_id = str(file_id)
        self.access_hash = str(access_hash)
        self.file_size = str(file_size)
        self.name = str(name)
        self.mime_type = str(mime_type)

        if caption_text:
            if isinstance(caption_text, TextMessage):
                self.caption_text = caption_text
        else:
            self.caption_text = None

        self.checksum = str(checksum) if checksum else "checkSum"
        self.algorithm = str(algorithm) if algorithm else "algorithm"
        self.file_storage_version = int(file_storage_version)

    def get_json_object(self):
        data = {
            "$type": MessageType.document_message,
            "fileId": self.file_id,
            "accessHash": self.access_hash,
            "fileSize": self.file_size,
            "name": self.name,
            "mimeType": self.mime_type,
            "thumb": None,
            "ext": None,
            "caption": self.caption_text.get_json_object() if self.caption_text else None,
            "checkSum": self.checksum,
            "algorithm": self.algorithm,
            "fileStorageVersion": self.file_storage_version

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

        file_id = json_dict.get('fileId', None)
        access_hash = json_dict.get('accessHash', None)
        file_size = json_dict.get('fileSize', None)
        name = json_dict.get('name', None)
        mime_type = json_dict.get('mimeType', None)

        caption_message = TextMessage.load_from_json(json_dict.get('caption', None))

        checksum = json_dict.get('checkSum', None)
        algorithm = json_dict.get('algorithm', None)
        file_storage_version = json_dict.get('fileStorageVersion', None)

        if (not file_id) or (not access_hash) or (name is None) or (file_size is None) or (mime_type is None):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(file_id=file_id, access_hash=access_hash, name=name, file_size=file_size,
                   mime_type=mime_type, file_storage_version=file_storage_version, caption_text=caption_message,
                   checksum=checksum, algorithm=algorithm)

    @staticmethod
    def is_video_message(json_dict):
        message_type = json_dict.get("$type", None)
        message_ext = json_dict.get("ext", None)
        document_type = message_ext.get("$type", None)

        return message_type == MessageType.document_message and document_type == DocumentType.video_document

    @staticmethod
    def is_photo_message(json_dict):
        message_type = json_dict.get("$type", None)
        message_ext = json_dict.get("ext", None)
        document_type = message_ext.get("$type", None)

        return message_type == MessageType.document_message and document_type == DocumentType.photo_document

    @staticmethod
    def is_voice_message(json_dict):
        message_type = json_dict.get("$type", None)
        message_ext = json_dict.get("ext", None)
        document_type = message_ext.get("$type", None)

        return message_type == MessageType.document_message and document_type == DocumentType.voice_document

    @staticmethod
    def is_raw_document_message(json_dict):
        message_type = json_dict.get("$type", None)
        message_ext = json_dict.get("ext", None)

        return message_type == MessageType.document_message and not message_ext
