import logging
from datetime import datetime


def parse_proxy(proxy_str):
    # Extract proxy details
    parts = proxy_str.strip().split(':')
    host = parts[0]
    port = parts[1]
    username = parts[2]
    password = parts[3]

    # Construct the proxy URL
    proxy_url = f"http://{username}:{password}@{host}:{port}"
    return proxy_url


def get_logger(logging_format='[%(asctime)s] [%(levelname)s] %(message)s', logging_file='logs.log'):
    class TimeFormatter(logging.Formatter):
        def formatTime(self, record, datefmt=None):
            ct = datetime.fromtimestamp(record.created)
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            return t

    # Create or retrieve the logger
    logger = logging.getLogger(__name__)

    # Check if the logger already has handlers to avoid adding them multiple times
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        formatter = TimeFormatter(logging_format)

        # Create a file handler
        file_handler = logging.FileHandler(logging_file, encoding='utf-8')
        file_handler.setFormatter(formatter)

        # Create a stream handler (for displaying logs in the terminal)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Add both handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

