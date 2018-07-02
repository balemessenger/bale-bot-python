import json as json_handler
from balebot.models.constants.errors import Error

from balebot.models.base_models.jsonable import Jsonable


class FileLocation(Jsonable):
    def __init__(self, file_id, access_hash, file_storage_version=1):
        self.file_id = str(file_id)
        self.access_hash = str(access_hash)
        self.file_storage_version = int(file_storage_version)

    def get_json_object(self):
        data = {
            "fileId": self.file_id,
            "accessHash": self.access_hash,
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
        file_storage_version = json_dict.get('fileStorageVersion', None)

        if (not file_id) or (not access_hash):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(file_id=file_id, access_hash=access_hash, file_storage_version=file_storage_version)
