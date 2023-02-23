# utf-8

from yuque import yuque_service
from utils import log_utils

logger = log_utils.get_logger("exporter")

if __name__ == '__main__':
    lib_dict = yuque_service.get_lib_dict()
    if lib_dict.__len__() > 0:
        yuque_service.download_lib_dict(lib_dict)
    else:
        logger.info("lib is empty")
