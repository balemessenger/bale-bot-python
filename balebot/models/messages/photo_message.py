import json as json_handler

from balebot.models.messages.document_message import DocumentMessage

from balebot.models.constants.document_type import DocumentType
from balebot.models.messages.text_message import TextMessage


class PhotoMessage(DocumentMessage):
    def __init__(self, file_id, access_hash, name, file_size, mime_type, thumb, width=80, height=80, ext_width=None,
                 ext_height=None, file_storage_version=None, caption_text=None, checksum=None, algorithm=None):

        super(PhotoMessage, self).__init__(file_id, access_hash, name, file_size, mime_type,
                                           caption_text, checksum, algorithm, file_storage_version)
        self.thumb = str(thumb)
        self.width = int(width)
        self.height = int(height)
        self.ext_width = int(ext_width) if ext_width else width
        self.ext_height = int(ext_height) if ext_height else height

    def get_json_object(self):

        data = super().get_json_object()
        data["thumb"] = {
            "width": self.width,
            "height": self.height,
            "thumb": self.thumb
        }
        data["ext"] = {
            "$type": DocumentType.photo_document,
            "width": self.ext_width,
            "height": self.ext_height,
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
            raise ValueError("json input has unacceptable format.")

        file_id = json_dict.get('fileId', None)
        access_hash = json_dict.get('accessHash', None)
        name = json_dict.get('name', None)
        file_size = json_dict.get('fileSize', None)
        mime_type = json_dict.get('mimeType', None)

        ext = json_dict.get('ext', None)
        ext_width = ext.get('width', None)
        ext_height = ext.get('height', None)

        thumb = json_dict.get('thumb', None)
        width = thumb.get('width', None)
        height = thumb.get('height', None)
        thumb_txt = thumb.get('thumb', None)

        file_storage_version = json_dict.get('fileStorageVersion', None)

        caption_message = TextMessage.load_from_json(json_dict.get('caption', None))

        checksum = json_dict.get('checkSum', None)
        algorithm = json_dict.get('algorithm', None)

        if (not file_id) or (not access_hash) or (name is None) or (file_size is None) or \
                (mime_type is None) or (width is None) or (height is None) or \
                (ext_width is None) or (ext_height is None) or (thumb_txt is None):
            raise ValueError("main parameters should have value.")

        return cls(file_id=file_id, access_hash=access_hash, name=name, file_size=file_size,
                   mime_type=mime_type, width=width, height=height, ext_width=ext_width, ext_height=ext_height,
                   thumb=thumb_txt, file_storage_version=file_storage_version, caption_text=caption_message,
                   checksum=checksum, algorithm=algorithm)
