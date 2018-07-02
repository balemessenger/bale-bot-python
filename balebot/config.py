import logging
import os


class Config:
    base_url = os.environ.get('BASE_URL', None) or "wss://api.bale.ai/v1/bots/"
    request_timeout = int(os.environ.get('REQUEST_TIMEOUT', None) or 5)
    # 0:print to output        1:use graylog       2:both 0 and 1
    use_graylog = os.environ.get('SDK_USE_GRAYLOG', None) or "0"
    source = os.environ.get('LOG_SOURCE', None) or "bot_source"
    graylog_host = os.environ.get('SDK_GRAYLOG_HOST', None) or "172.30.41.67"
    graylog_port = int(os.environ.get('SDK_GRAYLOG_PORT', None) or 12201)
    log_level = int(os.environ.get('SDK_LOG_LEVEL', None) or logging.DEBUG)
    log_facility_name = os.environ.get('SDK_LOG_FACILITY_NAME', None) or "python_bale_bot"
    monitoring_hash = os.environ.get('MONITORING_HASH', None) or "cabb3f498ac5a037f669f658f1be08c3-"
    real_time_fetch_updates = os.environ.get('REAL_TIME_FETCH_UPDATES', None) or True
    continue_last_processed_seq = os.environ.get('CONTINUE_LAST_PROCESSED_SEQ', None) or False
    timeInterval = os.environ.get('TIME_INTERVAL', None) or 1  # unit for time interval is second
    updates_number = os.environ.get('UPDATES_NUMBER', None) or 3
