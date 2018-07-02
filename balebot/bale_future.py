from asyncio import Future
import collections


class BaleFuture:
    def __init__(self, request_id, response_body_module, response_body_class,
                 success_callback=None, failure_callback=None, **kwargs):

        self.request_id = str(request_id)
        self.response_body_module = response_body_module
        self.response_body_class = response_body_class
        self.success_callback = success_callback if isinstance(success_callback, collections.Callable) else None
        self.failure_callback = failure_callback if isinstance(failure_callback, collections.Callable) else None
        self.user_data = kwargs if kwargs else {}

    def set_user_data(self, **kwargs):
        if kwargs:
            self.user_data.update(kwargs)

    def resolve(self, response):
        if self.success_callback:
            self.success_callback(response, self.user_data)

    def reject(self, response):
        if self.failure_callback:
            self.failure_callback(response, self.user_data)
