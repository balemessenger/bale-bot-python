from balebot.models.base_models import fat_seq_update

from balebot.models.base_models import response


class ServerUpdateFactory:
    @staticmethod
    def create_update(json_dict):
        update_type = json_dict.get("$type", None)

        if update_type == "Response":
            return response.Response(json_dict)

        elif update_type == "FatSeqUpdate":
            return fat_seq_update.FatSeqUpdate(json_dict)

        else:
            return
