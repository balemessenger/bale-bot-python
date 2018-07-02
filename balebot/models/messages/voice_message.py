import json as json_handler

from balebot.models.messages.document_message import DocumentMessage
from balebot.models.constants.errors import Error

from balebot.models.constants.document_type import DocumentType
from balebot.models.messages.text_message import TextMessage


class VoiceMessage(DocumentMessage):
    def __init__(self, file_id, access_hash, name, file_size, mime_type, duration, file_storage_version=None,
                 caption_text=None, checksum=None, algorithm=None):

        super(VoiceMessage, self).__init__(file_id, access_hash, name, file_size, mime_type,
                                           caption_text, checksum, algorithm, file_storage_version)
        self.duration = int(duration)

    def get_json_object(self):

        data = super().get_json_object()
        data["ext"] = {
            "$type": DocumentType.voice_document,
            "duration": self.duration
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
        name = json_dict.get('name', None)
        file_size = json_dict.get('fileSize', None)
        mime_type = json_dict.get('mimeType', None)

        ext = json_dict.get('ext', None)
        duration = ext.get('duration', None)

        file_storage_version = json_dict.get('fileStorageVersion', None)

        caption_message = TextMessage.load_from_json(json_dict.get('caption', None))

        checksum = json_dict.get('checkSum', None)
        algorithm = json_dict.get('algorithm', None)

        if (not file_id) or (not access_hash) or (not name) or (file_size is None) or (not mime_type) or (
                    duration is None):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(file_id=file_id, access_hash=access_hash, name=name, file_size=file_size,
                   mime_type=mime_type, duration=duration, file_storage_version=file_storage_version,
                   caption_text=caption_message, checksum=checksum, algorithm=algorithm)
