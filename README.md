# Bale bot python
[![Build Status](https://avatars1.githubusercontent.com/u/35299314?s=200&v=4)](https://github.com/balemessenger)

Python SDK and samples for [Bale bot messenger](https://developers.bale.ai).


### Register for an Access Token

You'll need to create your bot by [@Bot_Father](https://web.bale.ai/). Bot_Father gives you a Token to start.

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```python
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import *
from balebot.updater import Updater

updater = Updater(token="Bot_token",
                  loop=asyncio.get_event_loop())
bot = updater.bot
dispatcher = updater.dispatcher

```

__Note__: You need to set Config.py if you want to use the logger class


##### Simple communication with client

> Allows you to hear from client and answer.


```python
@dispatcher.message_handler(filters=TextFilter(keywords=["hello"]))  # filter text the client enter to bot
def hear(bot, update):
    message = TextMessage('Hello')
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
```


##### Sending a simple voice message:
__Note__:You should upload the voice file first.

> Allows you to send a voice message. (You can also send a document in the same way).


```python
def send_voice(bot, update):
    user_peer = update.get_effective_user()
    v_message = VoiceMessage(file_id=file_id, access_hash=access_hash, name="Hello", file_size='259969',
                                 mime_type="audio/mpeg",
                                 duration=20, file_storage_version=1)
    bot.send_message(v_message, user_peer, success_callback=success, failure_callback=failure)
```

##### Sending a generic template message:

__Note__:Generic Template Messages 
> Allows you to add cool text buttons to a general message.

```python
def ask_question(bot, update):
    general_message = TextMessage("a message")
    btn_list = [TemplateMessageButton(text="yes", value="yes", action=0),
                TemplateMessageButton(text="no", value="no", action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
```


##### Sending a generic purchase message:

> Allows you send a purchase message. Clients can pay the money requested by the message by pressing "pay" button.

```python

@dispatcher.message_handler(PhotoFilter())
def purchase_message(bot, update):
    message = update.get_effective_message()
    user_peer = update.get_effective_user()
    first_purchase_message = PurchaseMessage(msg=message, account_number=6037991067471130, amount=10,
                                             money_request_type=MoneyRequestType.normal)
    bot.send_message(first_purchase_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)
```

visit [bale-developers](https://developers.bale.ai) for more information

