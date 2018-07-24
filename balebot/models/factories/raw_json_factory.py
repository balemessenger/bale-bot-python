from balebot.models.messages import contact_message
from balebot.models.messages import location_message
from balebot.models.constants.raw_json_type import RawJsonType



class RawJsonFactory:
    @staticmethod
    def create_raw_json(json_dict):
        json_type = json_dict.get("dataType", None)

        if json_type == RawJsonType.contact:
            return contact_message.ContactMessage.load_from_json(json_dict)

        elif json_type == RawJsonType.location:
            return location_message.LocationMessage.load_from_json(json_dict)

        else:
            return None
