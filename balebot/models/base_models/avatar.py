import json as json_handler
from balebot.models.constants.errors import Error

from balebot.models.base_models.image_location import ImageLocation

from balebot.models.base_models.jsonable import Jsonable


class Avatar(Jsonable):
    def __init__(self, small_image=None, large_image=None, full_image=None):

        if small_image:
            if isinstance(small_image, ImageLocation):
                self.small_image = small_image
            else:
                raise ValueError(Error.unacceptable_object_type)
        else:
            self.small_image = None

        if large_image:
            if isinstance(large_image, ImageLocation):
                self.large_image = large_image
            else:
                raise ValueError(Error.unacceptable_object_type)
        else:
            self.large_image = None

        if full_image:
            if isinstance(full_image, ImageLocation):
                self.full_image = full_image
            else:
                raise ValueError(Error.unacceptable_object_type)
        else:
            self.full_image = None

    def get_json_object(self):

        data = {
            "smallImage": self.small_image.get_json_object(),
            "largeImage": self.large_image.get_json_object(),
            "fullImage": self.full_image.get_json_object(),
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

        small_image = ImageLocation.load_from_json(json_dict.get("smallImage", None)) \
            if json_dict.get("smallImage", None) else None
        large_image = ImageLocation.load_from_json(json_dict.get("largeImage", None)) \
            if json_dict.get("largeImage", None) else None
        full_image = ImageLocation.load_from_json(json_dict.get("fullImage", None)) \
            if json_dict.get("fullImage", None) else None

        return cls(small_image=small_image, large_image=large_image, full_image=full_image)
