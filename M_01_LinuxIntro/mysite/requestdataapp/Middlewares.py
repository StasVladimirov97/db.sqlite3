import time

from django.http import HttpRequest
from django.shortcuts import render


def set_useragent_on_request_middleware(get_response):
    print("initial call")

    def middleware(request: HttpRequest):
        print("before get_response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get_response")

        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.request_time = {}
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        time_delay = 10
        if not self.request_time:
            print('This first request after return server, the dictionary empty')
        else:
            if (round(time.time()) * 1) - self.request_time['time'] < time_delay \
                    and self.request_time['ip_address'] == request.META.get('REMOTE.ADDR'):
                print('less than 10 seconds elapsed for retry request')
                return render(request, 'requestdataapp/error-request.html')
        self.request_time = {'time': round(time.time()) * 1, 'ip_address': request.META.get('REMOTE.ADDR')}

        self.requests_count += 1
        print("requests count ", self.requests_count)
        response = self.get_response(request)
        print("responses count ", self.responses_count)
        self.responses_count += 1
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exception so far")
