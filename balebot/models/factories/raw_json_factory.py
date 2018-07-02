from balebot.models.base_models import contact
from balebot.models.base_models import location
from balebot.models.constants.raw_json_type import RawJsonType


class RawJsonFactory:
    @staticmethod
    def create_raw_json(json_dict):
        json_type = json_dict.get("dataType", None)

        if json_type == RawJsonType.contact:
            return contact.Contact.load_from_json(json_dict)

        elif json_type == RawJsonType.location:
            return location.Location.load_from_json(json_dict)

        else:
            return None
