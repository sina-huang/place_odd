import sys
import time
import logging
from logging.handlers import RotatingFileHandler  # 确保从 logging.handlers 导入

def get_logger(name, log_file,
               level=logging.INFO,
               console_level=logging.WARNING,
               file_mode='w',
               deduplicate=False):
    """
    获取日志器

    :param deduplicate: 是否启用日志去重功能，默认 False
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # 创建文件处理器
        file_handler = RotatingFileHandler(log_file, mode=file_mode, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(console_level)
        console_formatter = logging.Formatter(
            '[%(levelname)s] [%(name)s] %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)


        logger.propagate = False

    return logger


logger = get_logger(name="test", log_file="test.log")
print(type(logger))