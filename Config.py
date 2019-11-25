import logging
import os


class Config:
    base_url = os.environ.get('BASE_URL', "wss://api.bale.ai/v1/bots/")
    request_timeout = int(os.environ.get('REQUEST_TIMEOUT', 15))
    # 0:print to output        1:use graylog       2:both 0 and 1
    use_graylog = os.environ.get('SDK_USE_GRAYLOG', "2")
    graylog_host = os.environ.get('SDK_GRAYLOG_HOST', "127.0.0.1")
    graylog_port = int(os.environ.get('SDK_GRAYLOG_PORT', "12201"))
    log_level = int(os.environ.get('SDK_LOG_LEVEL', logging.DEBUG))
    log_facility_name = os.environ.get('SDK_LOG_FACILITY_NAME', "python_bale_bot")
    source = os.environ.get('LOG_SOURCE', "bot_source")
    heartbeat = int(os.environ.get("HEARTBEAT", 30))
