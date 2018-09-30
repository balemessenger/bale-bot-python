import unittest
from unittest.mock import MagicMock

from balebot.models.base_models import Peer
from balebot.models.client_requests import EditMessage
from balebot.models.messages import TextMessage


class TestEditMessage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        peer = Peer(peer_type="User", peer_id=1422775695,
                    access_hash="asdqweqwdasd")
        message = TextMessage("ASD")
        cls.update_request = EditMessage(updated_message=message, peer=peer, random_id=123465)

    def test_get_json_object(self):
        self.assertIsInstance(self.update_request.get_json_object(), dict)

    def test_get_json_str(self):
        self.assertIsInstance(self.update_request.get_json_str(), str)
