=========
Cron Jobs
=========

In practice, :program:`meetup2xibo` and :program:`summarize-m2x-logs` run
unattended as `cron`_ jobs.

Cron Setup
----------

:command:`Cron` runs jobs listed in a *crontab* file.
This file must be edited with the :command:`crontab` program::

   $ crontab -e

The example cron jobs below are written for the :command:`bash` shell.
Add this line to the crontab to select that shell::

   SHELL=/bin/bash

When a cron job produces any output to *stdout* or *stderr* (standard output
and standard error, respectively), cron can send those results via email.
Add this line to the crontab to specify the email recipient::

   MAILTO=chris.jones@example.com

The cron jobs run meetup2xibo, summarize-m2x-logs, and yesterday, all programs
installed by the meetup2xibo package.
The :command:`which` command will reveal where meetu2xibo and the other
programs were installed:

.. code-block:: console

   $ which meetup2xibo
   /home/joels/.virtualenvs/meetup2xibo/bin/meetup2xibo

Add this line to the crontab to extend the system path with the path to the
meetup2xibo programs::

   PATH=~/.virtualenvs/meetup2xibo/bin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

Meetup2xibo Cron Jobs
---------------------

Cron runs meetup2xibo frequently to keep the agenda displays up-to-date with
Meetup.com.
Most events start on the hour, at a quarter past, or half past the hour, so run
times are slightly offset ahead of event start times.

The following crontab line schedules ordinary meetup2xibo runs every 10 minutes::

   3,13,23,33,43,53 * * * * cd ~/meetup2xibo && . ./meetup2xibo.env && meetup2xibo -w

The :option:`-w <meetup2xibo -w>` option directs warnings to standard error; cron will send them
via email to the cron user.
Meetup2xibo will log info and higher messages to the default
:file:`meetup2xibo.log` file.

Late each day, cron runs meetup2xibo with two extra options:

- :option:`-c <meetup2xibo -c>` to log schedule conflicts

- :option:`-m <meetup2xibo -m>` to log all location mappings from Meetup.com's
  venue name and how-to-find-us fields to Xibo's location

This run is scheduled to avoid the every-10-minute runs.
The following crontab line schedules a schedule conflict and location mapping
meetup2xibo run every night before midnight::

   48 23 * * * cd ~/meetup2xibo && . ./meetup2xibo.env && meetup2xibo -w -c -m

.. _`summarizer-cron-job`:

Summarize-m2x-logs Cron Job
---------------------------

Cron runs summarize-m2x-logs early every morning to summarize the previous
day's meetup2xibo activity and mail the results to interested people.
The time was chosen to take place after daily log rotation, to have low impact
on computer resources, and to provide a morning email to administrators.
The following crontab line schedules summarize-m2x-logs while administrators
are sleeping::

   44 1 * * * YESTERDAY=`yesterday` ; summarize-m2x-logs
   -t "jmith@example.com events@example.com"
   -s "Meetup to Xibo Summary for ${YESTERDAY}"
   ~/meetup2xibo/meetup2xibo.log.${YESTERDAY}
   | ssmtp -t

These five lines must be combined into a single crontab line.

Yesterday's date is saved in ``YESTERDAY`` for substituion later on the line.
The :option:`-t <summarize-m2x-logs -t>` option selects email-formatted output
and provides a space-separated list of email recipients.
The :option:`-s <summarize-m2x-logs -s>` option provides the email subject with
yesterday's date inserted.
Summarize-m2x-logs takes yesterday's log file,
``~/meetup2xibo/meetup2xibo.log.${YESTERDAY}``, with yesterday's date appended
to the filename.

Cron pipes the email output to the :program:`sSMTP`, a lightweight mail
transport agent that handles only outbound emails.
On a more capable computer, :program:`sendmail` could be used instead.

.. _`cron`: https://en.wikipedia.org/wiki/Cron
