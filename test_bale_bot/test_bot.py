import unittest
from unittest.mock import MagicMock

from balebot.models.base_models import Peer
from balebot.models.messages import TextMessage
from balebot.bot import Bot
from balebot.models.base_models import Request


class TestBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = MagicMock()
        cls.bot.set_future.return_value = None
        cls.bot.send_request.return_value = None

    def test_update_message_content(self):
        message = TextMessage("ASD")
        peer = Peer(peer_type="User", peer_id=1422775695,
                    access_hash="asdqweqwdasd")
        self.assertIsInstance(Bot.edit_message(self.bot, message=message, user_peer=peer, random_id=13246),
                              Request)
