class Jsonable:
    def get_json_object(self):
        raise NotImplementedError

    def get_json_str(self):
        raise NotImplementedError

    @classmethod
    def load_from_json(cls, json):
        raise NotImplementedError
