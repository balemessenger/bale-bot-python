from balebot.handlers.handler import Handler
from balebot.models.base_models.fat_seq_update import FatSeqUpdate
from balebot.models.messages.template_response_message import TemplateResponseMessage
from balebot.models.messages.text_message import TextMessage


class CommandHandler(Handler):
    def __init__(self, commands, callback, include_template_response=False):
        super(CommandHandler, self).__init__(callback=callback)
        if isinstance(commands, str):
            commands = [commands.lower()]
        elif isinstance(commands, list):
            commands = [command.lower() for command in commands]
        self.commands = [(command[1:] if command.startswith("/") else command) for command in commands]
        self.include_template_response = include_template_response

    def check_update(self, update):
        if isinstance(update, FatSeqUpdate) and update.is_message_update():
            message = update.get_effective_message()
            if isinstance(message, TextMessage):
                message_text = message.text.lower()
            elif self.include_template_response and isinstance(message, TemplateResponseMessage):
                message_text = message.text_message.lower()
            else:
                return False

            if not message_text.startswith("/"):
                return False

            message_command = message_text[1:].split(" ")[0]

            return any(message_command == command for command in self.commands)
        return False

    def handle_update(self, dispatcher, update):
        return self.callback(dispatcher.bot, update)

    def is_default_handler(self):
        return False
