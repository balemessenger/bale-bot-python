import json as json_handler

from balebot.models.base_models.request_body import RequestBody
from balebot.models.constants.request_type import RequestType


class GetGroupApiStruct(RequestBody):
    def __init__(self, group_id, client_user_id):
        self.group_id = str(group_id)
        self.client_user_id = str(client_user_id)

    def get_json_object(self):
        data = {
            "$type": RequestType.get_group_api_struct,
            "groupId": self.group_id,
            "clientUserId": self.client_user_id,

        }

        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())
