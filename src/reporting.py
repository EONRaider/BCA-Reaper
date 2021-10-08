#!/usr/bin/env python3
# https://github.com/EONRaider/Keylogger

__author__ = "EONRaider @ keybase.io/eonraider"

import logging
from io import StringIO

"""
Set up handlers and formatters for logging and exfiltration of data.
"""

formatter = logging.Formatter(
    fmt="[%(name)s] %(asctime)s | %(levelname)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S")

# Main logger
main_handler = logging.StreamHandler()
main_handler.setLevel(logging.WARNING)
main_handler.setFormatter(formatter)

# Secondary streamer
streamer = StringIO()
stream_handler = logging.StreamHandler(stream=streamer)
stream_handler.setFormatter(formatter)

# Root logger
logging.basicConfig(level=logging.DEBUG,
                    handlers=[main_handler, stream_handler])


def set_logger(name: str = None) -> logging.Logger:
    return logging.getLogger(name)


def get_logs(flush_stream: bool = True) -> str:
    stream_contents = streamer.getvalue()
    if flush_stream is True:
        streamer.truncate(0)
        streamer.seek(0)
    return stream_contents
