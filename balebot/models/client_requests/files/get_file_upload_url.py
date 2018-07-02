import json as json_handler

from balebot.models.base_models.request_body import RequestBody
from balebot.models.constants.request_type import RequestType


class GetFileUploadUrl(RequestBody):
    def __init__(self, size, crc, file_type, is_server=False):
        self.size = int(size)
        self.crc = str(crc)
        self.is_server = bool(is_server)

        # it can be "photo" or "file"
        self.file_type = str(file_type)

    def get_json_object(self):
        data = {
            "$type": RequestType.get_file_upload_url,
            "size": self.size,
            "crc": self.crc,
            "isServer": self.is_server,
            'fileType': self.file_type,
        }

        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())
