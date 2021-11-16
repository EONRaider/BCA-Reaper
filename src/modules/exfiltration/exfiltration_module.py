#!/usr/bin/env python3
# https://github.com/EONRaider/BCA-Trojan

__author__ = "EONRaider @ keybase.io/eonraider"

from abc import abstractmethod, ABC


class ExfiltrationModule(ABC):
    def __init__(self, module):
        """Interface for the implementation of all exfiltrators.

        :param module: Instance of ExploitationModule from which the
            exfiltrator receive data by attaching itself as a
            subscriber.
        """
        self.module = module
        self.module.register_exfiltrator(self)

    @abstractmethod
    def update(self, message: [str, None]):
        """To be implemented with the logic specific to each
        exfiltration mechanism."""
        ...
