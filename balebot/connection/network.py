import asyncio
import traceback
import aiohttp
from balebot.utils.logger import Logger
from balebot.config import Config


class Network:
    """ network layer main class """

    def __init__(self, token, incoming_queue=None, outgoing_queue=None, loop=None):

        self.logger = Logger.get_logger()
        self._base_url = Config.base_url
        self._token = token
        self._running = False
        self._incoming_queue = incoming_queue or asyncio.Queue()
        self._outgoing_queue = outgoing_queue or asyncio.Queue()
        self._session = None
        self._ws = None
        self._loop = loop

        self._listener_task = None
        self._sender_task = None

    async def connect(self):
        if self._ws is None:

            try:
                self._session = aiohttp.ClientSession(loop=self._loop)
                self._ws = await self._session.ws_connect(self.construct_url())
                self.logger.debug('connect: {}'.format(self.construct_url()))
            except Exception as e:
                await self.disconnect()
                self.logger.error('connect error: {}'.format(e),
                                  extra={"tag": "err", "url": self.construct_url(), "error_type": type(e)})
                traceback.print_exc()

        elif self._ws.closed:
            try:
                if self._session.closed:
                    self._session = aiohttp.ClientSession(loop=self._loop)
                self._ws = await self._session.ws_connect(self.construct_url())
                self.logger.debug('reconnect: {}'.format(self.construct_url()))
            except Exception as e:
                await self.disconnect()
                self.logger.error('reconnect error: {}'.format(e),
                                  extra={"tag": "err", "url": self.construct_url(), "error_type": type(e)})
                traceback.print_exc()

        return self._ws

    def construct_url(self):
        return str(self._base_url + self._token)

    async def process(self):

        try:

            if await self.connect():

                self._listener_task = asyncio.ensure_future(self._ws.receive())
                self._sender_task = asyncio.ensure_future(self._outgoing_queue.get())

                main_tasks = [self._listener_task, self._sender_task]

                done, pending = await asyncio.wait(main_tasks, return_when=asyncio.FIRST_COMPLETED)

                if self._listener_task in done:
                    self.logger.debug('[transport] receiving :  {}'.format(self._listener_task.result()))
                    await self._incoming_queue.put(self._listener_task.result())
                else:
                    # self.logger.debug("listener task pended")
                    self._listener_task.cancel()

                if self._sender_task in done:
                    message = self._sender_task.result()
                    self._ws.send_str(str(message))
                    self.logger.debug('[transport] sending :  {}'.format(message))
                elif self._sender_task:
                    # self.logger.debug("sender tast pended")
                    self._sender_task.cancel()

        except Exception as ex:
            self.logger.error(ex, extra={"tag": "err"})
            traceback.print_exc()

    async def run(self):

        self._running = True
        while self._running:
            await self.process()
            await asyncio.sleep(0)

        if self._listener_task:
            self._listener_task.cancel()

        if self._sender_task:
            self._sender_task.cancel()

        await self.disconnect()

    def stop_network(self):
        self.logger.warning("network stopped working.")
        self._running = False

    async def disconnect(self):
        if self._ws:
            await self._ws.close()
        if self._session:
            await self._session.close()
        self.logger.warning("network connection disconnected.")

    def connected(self):
        if not self._session:
            return False
        elif not self._ws:
            return False
        elif self._session.closed or self._ws.closed:
            return False
        else:
            return True

    def send(self, item):
        self._outgoing_queue.put_nowait(item)
