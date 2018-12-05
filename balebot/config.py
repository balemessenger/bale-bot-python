import logging
import os


class Config:
    receive_timeout = int(os.environ.get("SESSION_TIMEOUT",60))
    base_url = os.environ.get('BASE_URL', "wss://api.bale.ai/v1/bots/")
    request_timeout = int(os.environ.get('REQUEST_TIMEOUT', 5))
    # 0:print to output        1:use graylog       2:both 0 and 1
    use_graylog = os.environ.get('SDK_USE_GRAYLOG', "0")
    source = os.environ.get('LOG_SOURCE', "bot_source")
    graylog_host = os.environ.get('SDK_GRAYLOG_HOST', "172.30.41.67")
    graylog_port = int(os.environ.get('SDK_GRAYLOG_PORT', 12201))
    log_level = int(os.environ.get('SDK_LOG_LEVEL', logging.DEBUG))
    log_facility_name = os.environ.get('SDK_LOG_FACILITY_NAME', "python_bale_bot")
    monitoring_hash = os.environ.get('MONITORING_HASH', "SADJSDSDas4d2asf41f2a2faasd45sas")
    real_time_fetch_updates = os.environ.get('REAL_TIME_FETCH_UPDATES', True)
    continue_last_processed_seq = os.environ.get('CONTINUE_LAST_PROCESSED_SEQ', False)
    timeInterval = int(os.environ.get('TIME_INTERVAL', 1))  # unit for time interval is second)
    updates_number = int(os.environ.get('UPDATES_NUMBER', 3))
    heartbeat = int(os.environ.get("HEARTBEAT", 30))
