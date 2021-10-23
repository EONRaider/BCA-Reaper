#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

from pathlib import Path

from src.modules.exploitation.exploitation_module import ExploitationModule
from src.modules.exfiltration.exfiltration_module import ExfiltrationModule


class File(ExfiltrationModule):
    def __init__(self, *,
                 module: ExploitationModule,
                 file_path: [str, Path]):
        """Exfiltrate data to a file on the local system.

        Args:
            module: Instance of ExploitationModule to which the
                exfiltrator receive data by attaching itself as a
                subscriber.
            file_path: A string or instance of pathlib.Path containing
                the absolute path to the location where the file will
                be written.
        """

        super().__init__(module)
        self.file_path = file_path

    def update(self, message: str) -> None:
        """Write each report on a new line of a text file with the
        specified path."""
        if self.module.has_data is True:
            with open(file=self.file_path, mode="a", encoding="utf_8") as file:
                file.write(f"{message}\n")
