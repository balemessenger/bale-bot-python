import asyncio
import pickle
import signal
import traceback
from collections import namedtuple

import redis

from balebot.config import Config
from balebot.dispatcher import Dispatcher
from balebot.utils.logger import Logger

redis_db = redis.StrictRedis(host=Config.redis_host, port=Config.redis_port, db=Config.redis_db) \
    if Config.state_holder else None
BotState = namedtuple('BotState', ['conversation_next_step_handlers', 'conversation_data'])


class Updater:
    def __init__(self, token, base_url=Config.base_url, loop=None):

        self.logger = Logger.get_logger()

        if not token:
            raise ValueError("`token` did't passed")

        if not base_url:
            raise ValueError("`base_url` did't passed")

        self.token = token
        self.timeout = Config.request_timeout

        self.bale_futures = []

        self._loop = asyncio.get_event_loop() if not loop else loop

        self.dispatcher = Dispatcher(loop=self._loop,
                                     token=self.token, base_url=base_url,
                                     bale_futures=self.bale_futures)

        self.running = False

    def run(self, stop_after=None):
        signal.signal(signal.SIGTERM, self.stop)
        if Config.state_holder:
            bot_previous_state = redis_db.get(self.token)
            bot_previous_state = pickle.loads(bot_previous_state) if bot_previous_state else None
            self.dispatcher.conversation_next_step_handlers, self.dispatcher.conversation_data = \
                (bot_previous_state.conversation_next_step_handlers, bot_previous_state.conversation_data) \
                    if bot_previous_state else ({}, {})

        asyncio.ensure_future(self._run_dispatcher())
        asyncio.ensure_future(self.dispatcher.bot.network.run())

        try:
            if isinstance(stop_after, int) or isinstance(stop_after, float):
                self._stop_after(stop_after)

            self._loop.run_forever()

        except Exception as e:
            self.logger.error("exception :  {} ,  {}".format(type(e), e), extra={"tag": "err"})
            traceback.print_exc()
        finally:
            self.stop()

    def stop(self):
        if Config.state_holder:
            redis_db.set(self.token, pickle.dumps(
                BotState(conversation_next_step_handlers=self.dispatcher.conversation_next_step_handlers,
                         conversation_data=self.dispatcher.conversation_data)))
        self.dispatcher.bot.network.stop_network()
        self._stop_dispatcher()
        self._loop.stop()

    def _run_dispatcher(self):
        return self.dispatcher.run()

    def _stop_dispatcher(self):
        self.dispatcher.stop()

    def _stop_after(self, delay):
        self._loop.call_later(delay=delay, callback=self.stop)

    def network_connected(self):
        return self.dispatcher.bot.network.connected()

    def connect_network(self):
        asyncio.ensure_future(self.dispatcher.bot.network.connect())
