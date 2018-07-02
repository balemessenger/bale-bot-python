import json as json_handler

from balebot.models.base_models.jsonable import Jsonable
from balebot.models.constants.errors import Error

from balebot.models.base_models.file_location import FileLocation


class ImageLocation(Jsonable):
    def __init__(self, width, height, file_size, file_location):
        self.width = int(width)
        self.height = int(height)
        self.file_size = int(file_size)
        if isinstance(file_location, FileLocation):
            self.file_location = file_location
        else:
            raise ValueError(Error.unacceptable_object_type)

    def get_json_object(self):
        data = {
            "width": self.width,
            "height": self.height,
            "fileSize": self.file_size,
            "fileLocation": self.file_location.get_json_object()
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

        width = json_dict.get("width", None)
        height = json_dict.get("height", None)
        file_size = json_dict.get("fileSize", None)
        file_location = FileLocation.load_from_json(json_dict.get("fileLocation", None))

        if (width is None) or (height is None) or (file_size is None) or (file_location is None):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(width=width, height=height, file_size=file_size, file_location=file_location)
