# utf-8

from datetime import datetime
from utils import file_utils
import logging


def get_logger(caller_name):
    format_str = '%(asctime)s ' \
                 '%(levelname)s ' \
                 '[%(threadName)s--%(thread)d] ' \
                 '%(message)s'
    logging.basicConfig(format=format_str, level="DEBUG")
    logger = logging.getLogger(caller_name)
    datetime_now = datetime.now().strftime("%Y%m%d%H%M%S")
    log_dir = './log'
    file_utils.mkDir(log_dir)
    logs = logging.FileHandler(log_dir + "/" + caller_name + '_' + datetime_now + '.log')
    formatter = logging.Formatter(format_str)
    logs.setFormatter(formatter)
    logger.addHandler(logs)
    return logger


