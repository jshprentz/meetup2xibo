=======
Logging
=======

:program:`Meetup2xibo` logs its activity to a log file and optionally to the
console *(stderr).*
Command line flags control which log messages should be directed to which
destinations.
Supporting program :program:`summarize-m2x-logs` summarizes log files,
reporting on meetup2xibo runs and event changes.

Log Destinations
----------------

By default, meetup2xibo writes log messages to file :file:`meetup2xibo.log` in
the current directory.
The :option:`-t <meetup2xibo -l>` option can specify an alternate path to the
log file.
The :option:`-v <meetup2xibo -v>` option adds console output.
The :option:`-w <meetup2xibo -w>` option adds console output and limits the
console log level to warnings and errors.

Log Levels
----------

By default, meetup2xibo logs only info, warning, and error messages.
The :option:`-d <meetup2xibo -d>` option adds debug level messages, which help
software developers.
As described above, the :option:`-w <meetup2xibo -w>` option adds console
output and limits the console log level to warnings and errors.
:numref:`Table %s <log-levels>` summarizes the log levels and the impact of the
:option:`-d <meetup2xibo -d>` and :option:`-w <meetup2xibo -w>` flags.

.. tabularcolumns:: |L|L|C|C|C|

.. _log-levels:

.. table:: Meetup2xibo Log Levels
   :align: center

   +-----------+---------------------+---------+---------+-------------------+
   | Log Level | Reports             | Default | -d Flag | -w Flag (console) |
   +===========+=====================+=========+=========+===================+
   | Error     | Failures            | ✔       | ✔       | ✔                 |
   +-----------+---------------------+---------+---------+-------------------+
   | Warning   | Abnormal conditions | ✔       | ✔       | ✔                 |
   +-----------+---------------------+---------+---------+-------------------+
   | Info      | Routine operations  | ✔       | ✔       |                   |
   +-----------+---------------------+---------+---------+-------------------+
   | Debug     | Developer details   |         | ✔       |                   |
   +-----------+---------------------+---------+---------+-------------------+

Log Summaries
-------------

Summarize-m2x-logs summarizes one or more meetup2xibo log files.
The summary includes:

- Counts of meetup2xibo runs, by version
- Lists of schedule conflicts
- Lists of events inserted, updated, deleted, and retired
- Field-by-field details of updated events
- Warnings about missing event locations
- Warnings about special event locations no longer needed
- Spreadsheet showing conversions from Meetup.com locations to Xibo locations

:ref:`summarizer-cron-job` describes how to run summarize-m2x-logs daily and send the
HTML-formatted results via email.
:numref:`Figure %s <summary-email>` shows an example of the daily email message.

.. figure:: /images/screenshots/summary-email.png
   :alt: Screenshot showing part of a daily email summary of meetup2xibo logs
   :name: summary-email
   :align: center

   The daily summary email message counts meetup2xibo runs, lists schedule
   conflicts, and lists Xibo event changes.

An email message attachment contains a CSV formatted file listing the
conversions from Meetup.com venue name and how-to-find-us fields to Xibo
locations.
An administrator can review the CSV file in Microsoft Excel or another
spreadsheet program.
The administrator can resolve location conversion anomalies by editing the
Meetup.com event or by adding a new location phrase or special location to the
meetup2xibo configuration.
:numref:`Figure %s <location-spreadsheet>` shows an example of the location conversion
spreadsheet.

.. figure:: /images/screenshots/location-spreadsheet.png
   :alt: Screenshot of location conversions in spreadsheet format with columns
         for location, venue, find us, example meetup, and example URL
   :name: location-spreadsheet
   :align: center

   The first several lines of location conversions list in CSV format and
   viewed as a spreadsheet in Microsoft Excel.

