import asyncio
import traceback

from balebot.bot import Bot
from balebot.connection.network import Network
from balebot.dispatcher import Dispatcher
from balebot.utils.logger import Logger
from balebot.config import Config


class Updater:
    def __init__(self, token, loop=None):

        self.logger = Logger.get_logger()

        if not token:
            raise ValueError("`token` did't passed")

        self.token = token
        self.base_url = Config.base_url
        self.timeout = Config.request_timeout

        self.bale_futures = []

        self._incoming_queue = asyncio.Queue()
        self._outgoing_queue = asyncio.Queue()

        self._loop = asyncio.get_event_loop() if not loop else loop

        self._network = Network(base_url=self.base_url,
                                token=self.token,
                                incoming_queue=self._incoming_queue,
                                outgoing_queue=self._outgoing_queue,
                                loop=self._loop)

        self.bot = Bot(loop=self._loop,
                       network=self._network,
                       bale_futures=self.bale_futures,
                       timeout=self.timeout)

        self.dispatcher = Dispatcher(bot=self.bot,
                                     bale_futures=self.bale_futures,
                                     timeout=self.timeout,
                                     incoming_queue=self._incoming_queue,
                                     outgoing_queue=self._outgoing_queue)

        self.running = False

    def run(self, stop_after=None):

        asyncio.ensure_future(self._run_dispatcher())
        asyncio.ensure_future(self._network.run())

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
        self._network.stop_network()
        self._stop_dispatcher()
        self._loop.stop()

    def _run_dispatcher(self):
        return self.dispatcher.run()

    def _stop_dispatcher(self):
        self.dispatcher.stop()

    def _stop_after(self, delay):
        self._loop.call_later(delay=delay, callback=self.stop)

    def network_connected(self):
        return self._network.connected()

    def connect_network(self):
        asyncio.ensure_future(self._network.connect())
