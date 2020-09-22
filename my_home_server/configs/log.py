import os
import sys
import logging
import my_home_server.configs.config as config

from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter('%(asctime)s %(levelname)s --- %(module)s:%(lineno)d @@@ %(message)s')
LOG_FILE = f"{config.LOG_REPOSITORY}/myhome-server.log"


if not os.path.exists(config.LOG_REPOSITORY):
    os.mkdir(config.LOG_REPOSITORY)


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    sql_logger = logging.getLogger('sqlalchemy.engine')
    sql_logger.setLevel(logging.INFO)

    logger.setLevel(logging.INFO)

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())

    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False

    return logger
