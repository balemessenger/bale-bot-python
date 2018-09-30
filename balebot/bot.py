import functools
import asyncio
import aiohttp
import io
import sys
from PIL import Image
from balebot.models.base_models import response
from balebot.connection.network import Network
from balebot.bale_future import BaleFuture
from balebot.models.client_requests import *

from balebot.models.base_models import BotQuotedMessage, FatSeqUpdate, GroupPeer, Request, UserPeer
from balebot.models.client_requests.sequence.get_last_sequence import GetLastSequence
from balebot.models.constants.request_to_response_mapper import RequestToResponseMapper
from balebot.models.constants.service_type import ServiceType
from balebot.models.messages import BaseMessage, TextMessage, PhotoMessage, DocumentMessage
from balebot.utils.util_functions import get_file_crc32, get_file_size, get_file_buffer, get_image_thumbnails


class Bot:
    def __init__(self, loop, token, incoming_queue, outgoing_queue, bale_futures, timeout):
        self._loop = loop
        self.network = Network(token=token,
                               incoming_queue=incoming_queue,
                               outgoing_queue=outgoing_queue,
                               loop=loop)

        self._bale_futures = bale_futures
        self.timeout = timeout

    def set_future(self, request_id, request_body, success_callback=None, failure_callback=None, **kwargs):
        response_body_module, response_body_class = RequestToResponseMapper.get_response(request_body)
        bale_future = BaleFuture(request_id, response_body_module, response_body_class,
                                 success_callback, failure_callback, **kwargs)
        self._bale_futures.append(bale_future)

        self._loop.call_later(self.timeout, functools.partial(self.timeout_future, bale_future))

    def timeout_future(self, bale_future):
        if bale_future in self._bale_futures:
            bot_timeout_json = {"body": {"tag": "CLIENT_REQUEST_TIMEOUT"}}
            error_response = response.Response(bot_timeout_json)
            bale_future.reject(error_response)
            self._bale_futures.remove(bale_future)

    def send_request(self, request_data):
        self.network.send(request_data)

    def reply(self, update, message, success_callback=None, failure_callback=None, **kwargs):
        if isinstance(update, FatSeqUpdate) and update.is_message_update():
            message_id = update.body.random_id
            user_peer = update.get_effective_user()
            if isinstance(message, BaseMessage):
                return self.send_message(message, user_peer,
                                         BotQuotedMessage(message_id, user_peer),
                                         success_callback=success_callback,
                                         failure_callback=failure_callback,
                                         **kwargs)
            else:
                return self.send_message(TextMessage(message), user_peer,
                                         BotQuotedMessage(message_id, user_peer),
                                         success_callback=success_callback,
                                         failure_callback=failure_callback,
                                         **kwargs)

    def respond(self, update, message, success_callback=None, failure_callback=None, **kwargs):
        user_peer = update.get_effective_user()
        if isinstance(message, BaseMessage):
            return self.send_message(message, user_peer,
                                     success_callback=success_callback,
                                     failure_callback=failure_callback,
                                     **kwargs)
        else:
            return self.send_message(TextMessage(message), user_peer,
                                     success_callback=success_callback,
                                     failure_callback=failure_callback,
                                     **kwargs)

    # messaging
    def send_message(self, message, peer, quoted_message=None, random_id=None, success_callback=None,
                     failure_callback=None, **kwargs):
        receiver = peer
        request_body = SendMessage(message=message, receiver_peer=receiver,
                                   quoted_message=quoted_message, random_id=random_id)
        request = Request(service=ServiceType.Messaging, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    def edit_message(self, message, user_peer, random_id, success_callback=None, failure_callback=None,
                     **kwargs):
        text_message = message
        receiver = user_peer
        request_body = EditMessage(updated_message=text_message, peer=receiver, random_id=random_id)
        request = Request(service=ServiceType.Messaging, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    # group
    def create_group(self, title, success_callback=None, failure_callback=None, **kwargs):
        request_body = CreateGroup(title)
        request = Request(service=ServiceType.Groups, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    def get_group_api_struct(self, group_id, client_user_id, success_callback=None, failure_callback=None, **kwargs):
        request_body = GetGroupApiStruct(group_id=group_id, client_user_id=client_user_id)
        request = Request(service=ServiceType.Groups, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    def invite_user(self, group_peer_id, group_peer_access_hash, user_peer_id,
                    user_peer_access_hash, success_callback=None, failure_callback=None, **kwargs):
        group_peer = GroupPeer(peer_id=group_peer_id, access_hash=group_peer_access_hash)
        user_peer = UserPeer(peer_id=user_peer_id, access_hash=user_peer_access_hash)
        request_body = InviteUser(group_peer=group_peer, user_peer=user_peer)
        request = Request(service=ServiceType.Groups, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    # sequence-update
    def get_difference(self, seq, how_many, success_callback=None, failure_callback=None, **kwargs):
        request_body = GetDifference(seq=seq, how_many=how_many)
        request = Request(service=ServiceType.SequenceUpdate, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    # last_sequence
    def get_last_seq(self, success_callback=None, failure_callback=None, **kwargs):
        request_body = GetLastSequence()
        request = Request(service=ServiceType.SequenceUpdate, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    # file
    def get_file_download_url(self, file_id, user_id, file_type, file_version=1, is_server=False,
                              is_resume_upload=False, success_callback=None, failure_callback=None, **kwargs):
        request_body = GetFileDownloadUrl(file_id, user_id, file_type, file_version, is_server, is_resume_upload)
        request = Request(service=ServiceType.Files, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    def get_file_upload_url(self, size, crc, file_type, is_server=False,
                            success_callback=None, failure_callback=None, **kwargs):
        request_body = GetFileUploadUrl(size, crc, file_type, is_server)
        request = Request(service=ServiceType.Files, body=request_body)
        self.set_future(request.id, request_body, success_callback, failure_callback, **kwargs)
        self.send_request(request.get_json_str())
        return request

    def download_file(self, file_id, user_id, file_type="file", success_callback=None, failure_callback=None, **kwargs):

        future = BaleFuture(request_id=None, response_body_module=None, response_body_class=None,
                            success_callback=success_callback, failure_callback=failure_callback, **kwargs)

        def file_download_url_success(result, user_data):
            async def get_data(download_url):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(download_url) as download_response:
                            status = download_response.status

                            if status == 200:
                                byte_stream = await download_response.content.read()
                                future.set_user_data(byte_stream=byte_stream)
                                future.resolve(response=None)
                            else:
                                future.reject(response=None)
                except Exception as e:
                    future.reject(response=None)
            url = result.body.url
            asyncio.ensure_future(get_data(url))

        def file_download_url_failure(result, user_data):
            future.reject(response=result)

        self.get_file_download_url(file_id, user_id, file_type,
                                   success_callback=file_download_url_success,
                                   failure_callback=file_download_url_failure)

    def upload_file(self, file, file_type, success_callback=None, failure_callback=None, **kwargs):

        future = BaleFuture(request_id=None, response_body_module=None, response_body_class=None,
                            success_callback=success_callback, failure_callback=failure_callback, **kwargs)

        buffer = get_file_buffer(file=file)
        if buffer is None:
            future.reject(response=None)
            return

        file_size = get_file_size(buffer)
        file_crc32 = get_file_crc32(buffer)

        def file_upload_url_success(result, user_data):
            file_id = result.body.file_id
            user_id = result.body.user_id
            url = result.body.url
            dup = result.body.dup

            data = buffer
            headers = {'filesize': str(file_size)}

            async def upload_data():
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.put(url, data=data, headers=headers) as upload_response:
                            status = upload_response.status
                            if status == 200:
                                future.set_user_data(file_id=file_id, user_id=user_id, url=url, dup=dup)
                                future.resolve(response=None)
                            else:
                                future.reject(response=None)
                except Exception as e:
                    future.reject(response=None)
            asyncio.ensure_future(upload_data())

        def file_upload_url_failure(result, user_data):
            future.reject(response=result)

        self.get_file_upload_url(size=file_size, crc=file_crc32, file_type=file_type,
                                 success_callback=file_upload_url_success,
                                 failure_callback=file_upload_url_failure)

    def send_photo(self, user_peer, image, caption_text="", name="", file_storage_version=1, mime_type="image/jpeg",
                   success_callback=None, failure_callback=None, **kwargs):
        image_buffer = get_file_buffer(file=image)
        file_size = sys.getsizeof(image_buffer)
        im = Image.open(io.BytesIO(image_buffer))
        width, height = im.size
        thumb = get_image_thumbnails(im)

        def success_upload_image(user_data, server_response):
            file_id = str(server_response.get("file_id", None))
            access_hash = str(server_response.get("user_id", None))
            photo_message = PhotoMessage(file_id=file_id, access_hash=access_hash, name=name, file_size=file_size,
                                         mime_type=mime_type, file_storage_version=file_storage_version, width=width,
                                         height=height, caption_text=TextMessage(text=caption_text), thumb=thumb)
            self.send_message(message=photo_message, peer=user_peer, success_callback=success_callback,
                              failure_callback=failure_callback, kwargs=kwargs)

        self.upload_file(file=image, file_type="file", success_callback=success_upload_image,
                         failure_callback=failure_callback)

    def send_document(self, update, doc_file, mime_type, caption_text="", file_type="file", name="",
                      file_storage_version=1, success_callback=None, failure_callback=None, **kwargs):
        file_size = sys.getsizeof(doc_file)

        def success_upload_document(user_data, server_response):
            file_id = str(server_response.get("file_id", None))
            access_hash = str(server_response.get("user_id", None))
            document_message = DocumentMessage(file_id=file_id, access_hash=access_hash, name=name,
                                               file_size=file_size, mime_type=mime_type,
                                               caption_text=TextMessage(text=caption_text),
                                               file_storage_version=file_storage_version)
            self.respond(update=update, message=document_message, success_callback=success_callback,
                         failure_callback=failure_callback, kwargs=kwargs)

        self.upload_file(file=doc_file, file_type=file_type, success_callback=success_upload_document,
                         failure_callback=failure_callback)
