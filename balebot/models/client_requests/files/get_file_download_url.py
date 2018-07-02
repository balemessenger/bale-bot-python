import json as json_handler

from balebot.models.base_models.request_body import RequestBody
from balebot.models.constants.request_type import RequestType


class GetFileDownloadUrl(RequestBody):
    def __init__(self, file_id, user_id, file_type, file_version=1, is_server=False, is_resume_upload=False):
        self.file_id = str(file_id)
        self.user_id = str(user_id)
        self.file_version = int(file_version)
        self.is_server = bool(is_server)
        self.is_resume_upload = bool(is_resume_upload)

        # it can be "photo" or "file"
        self.file_type = str(file_type)

    def get_json_object(self):
        data = {
            "$type": RequestType.get_file_download_url,
            "fileId": self.file_id,
            "userId": self.user_id,
            "fileVersion": self.file_version,
            "isServer": self.is_server,
            "isResumeUpload": self.is_resume_upload,
            'fileType': self.file_type,
        }

        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())
