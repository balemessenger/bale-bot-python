import json as json_handler

from balebot.models.base_models.image_location import ImageLocation
from balebot.models.messages.base_message import BaseMessage
from balebot.models.constants.errors import Error

from balebot.models.constants.message_type import MessageType


class StickerMessage(BaseMessage):
    def __init__(self, sticker_id=None, sticker_collection_id=None, sticker_collection_access_hash=None,
                 fast_preview=None, image512=None, image256=None):
        self._sticker_id = str(sticker_id) if sticker_id else None
        self._sticker_collection_id = str(sticker_collection_id) if sticker_collection_id else None
        self._sticker_collection_access_hash = str(
            sticker_collection_access_hash) if sticker_collection_access_hash else None
        self._fast_preview = list(fast_preview) if fast_preview else None

        if image512:
            if isinstance(image512, ImageLocation):
                self._image512 = image512
            else:
                raise ValueError(Error.unacceptable_object_type)
        else:
            self._image512 = None

        if image256:
            if isinstance(image256, ImageLocation):
                self._image256 = image256
            else:
                raise ValueError(Error.unacceptable_object_type)
        else:
            self._image256 = None

    def get_json_object(self):

        data = {
            "$type": MessageType.sticker_message,
            "stickerId": self._sticker_id,
            "stickerCollectionId": self._sticker_collection_id,
            "stickerCollectionAccessHash": self._sticker_collection_access_hash,
            "fastPreview": self._fast_preview,
            "image512": self._image512.get_json_object() if self._image512 else None,
            "image256": self._image256.get_json_object() if self._image256 else None,

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

        sticker_id = json_dict.get("stickerId", None)
        sticker_collection_id = json_dict.get("stickerCollectionId", None)
        sticker_collection_access_hash = json_dict.get("stickerCollectionAccessHash", None)
        fast_preview = json_dict.get("fastPreview ", None)
        image512 = ImageLocation.load_from_json(json_dict.get("image512", None)) if json_dict.get("image512",
                                                                                                  None) else None
        image256 = ImageLocation.load_from_json(json_dict.get("image256", None)) if json_dict.get("image256",
                                                                                                  None) else None

        return cls(sticker_id=sticker_id, sticker_collection_id=sticker_collection_id,
                   sticker_collection_access_hash=sticker_collection_access_hash, fast_preview=fast_preview,
                   image512=image512, image256=image256)
