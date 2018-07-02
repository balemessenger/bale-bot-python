import logging
import graypy

from balebot.config import Config


class Logger:
    logger = None

    @staticmethod
    def init_logger():

        use_graylog = Config.use_graylog
        source = Config.source
        graylog_host = Config.graylog_host
        graylog_port = Config.graylog_port
        log_level = Config.log_level
        log_facility_name = Config.log_facility_name

        temp_logger = logging.getLogger(log_facility_name)
        temp_logger.setLevel(log_level)

        log_handlers = []

        if use_graylog == "0":
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s  %(filename)s:%(lineno)d  %(levelname)s:\n"%(message)s"'
            )
            handler.setFormatter(formatter)
            log_handlers.append(handler)

        elif use_graylog == "1" and graylog_host and source and graylog_port is not None \
                and isinstance(graylog_port, int):
            log_handlers.append(graypy.GELFHandler(host=graylog_host, port=graylog_port, localname=source))

        elif use_graylog == "2" and graylog_host and source and graylog_port is not None \
                and isinstance(graylog_port, int):
            handler1 = graypy.GELFHandler(host=graylog_host, port=graylog_port, localname=source)

            handler2 = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s  %(filename)s:%(lineno)d  %(levelname)s:\n"%(message)s"'
            )
            handler2.setFormatter(formatter)

            log_handlers.append(handler1)
            log_handlers.append(handler2)

        for log_handler in log_handlers:
            temp_logger.addHandler(log_handler)

        Logger.logger = temp_logger
        return Logger.logger

    @staticmethod
    def get_logger():
        if Logger.logger:
            return Logger.logger
        else:
            return Logger.init_logger()
