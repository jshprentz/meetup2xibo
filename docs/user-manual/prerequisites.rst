=============
Prerequisites
=============

Computing Environment
---------------------

- Linux or maybe Windows
- Internet
- Network to Xibo CMS via HTTPS
- Python 3.5, 3.6, or 3.7
- Python virtual environment recommended

Meetup2xibo was developed, tested, and run on computers with Ubuntu, a Linux
operating system.
Meetup2xibo has no dependencies on Ubuntu or Linux; it should run on Windows,
macOS, Raspberry Pi, or anywhere Python is available.

Meetup2xibo requires an internet connection to access Meetup.com.

Meetup2xibo requires network connection to your Xibo CMS.
If the Xibo CMS runs on a private network, meetup2xibo must also run on that
network.

Meetup2xibo connects securely to the Xibo CMS via HTTPS.
The Xibo CMS must be configured for secure HTTPS access as described by
"`Xibo for Docker on Linux`_."

Meetup2xibo was coded with the Python programming language.
Python must be installed to run meetup2xibo.
Meetup2xibo has been tested successfully with Python 3.5, 3.6, and 3.7

Meetup2xibo is distributed as a Python package.
It has dependencies on several other Python packages.
The Python Packaging Authority recommends creating a Python virtual environment
to keep meetup2xibo and its dependencies from conflicting with other Python
packages.
See "`Installing packages using pip and virtual environments`_."

Skills Needed
-------------

- Run commands from Linux shell
- Schedule cron jobs
- Edit configuration files
- Access Xibo CMS as administrator

You must be able to run commands on your computer.
On Linux, you can use a terminal window to enter commands.
On Windows, you can use a command or PowerShell window.
From a remote computer, you can connect via ssh to run commands.

You must be able to schedule commands on your computer to run meetup2xibo
periodically.
On Linux, setup cron jobs.
On Windows, use Windows Task Scheduler.

You must be able to use a text editor to edit configuration files.

You must have administrative access to your Xibo CMS to create dataset,
layouts, schedules, and users.

.. _`Installing packages using pip and virtual environments`: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
.. _`Xibo for Docker on Linux`: https://xibo.org.uk/docs/setup/xibo-for-docker-on-linux
