import unittest
from unittest.mock import MagicMock

from balebot.models.server_responses.messaging.message_edited import MessageEdited


class TestMessageEdited(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.edit_message_response_body = '{"seq":"2090","date":"1536053835915"}'

    def test_message_edited(self):
        message_edited_body = MessageEdited(self.edit_message_response_body)
        self.assertEqual(message_edited_body.date, '1536053835915')
        self.assertEqual(message_edited_body.seq, '2090')
