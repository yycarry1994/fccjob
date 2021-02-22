import time
import logging
import traceback

from django.http import HttpResponse
from sentry_sdk import capture_exception, capture_message

from interview import dingtalk

logger = logging.getLogger(__name__)


def performance_logger_middleware(get_response):
    def middleware(request):
        start_time = time.time()
        response = get_response(request)
        duration = time.time() - start_time
        response['X-Page-Duration-ms'] = int(duration * 1000)
        logger.info("{} {} {}".format(duration, request.path, request.GET.dict()))
        return response

    return middleware


class PerformanceAndExceptionLoggerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        response['X-Page-Duration-ms'] = int(duration * 1000)
        logger.info("{} {} {}".format(duration, request.path, request.GET.dict()))
        if duration > 300:
            capture_message('slow request for url:{} with duration:{}'.format(request.build_absolute_uri(), duration))

        return response

    def process_exception(self, request, exception):
        if exception:

            message = "url:{url} ** msg:{error} ````{tb}````".format(
                url=request.build_absolute_uri(),
                error=repr(exception),
                tb=traceback.format_exc()
            )

            logger.warning(message)

            # send dingtalk message
            dingtalk.send(message)

            # capture exception to sentry
            capture_exception(exception)

        return HttpResponse("ERROR processing the request, please contact the system administrator", status=500)