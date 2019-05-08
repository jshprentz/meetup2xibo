====================
Meetup2Xibo Overview
====================

.. figure:: /images/diagrams/meetup2xibo-event-data-flow.png
   :alt: Diagram showing the event data flow from Meetup.com to Xibo
   :name: meetup2xibo-event-data-flow

   Meetup2xibo retrieves event data from Meetup.com.
   Meetup2xibo edits the Meetup.com event data.
   Meetup2xibo inserts, updates, and deletes event data stored in a Xibo CMS
   dataset.
   Ticker widgets in Xibo layouts retrieve and display the event data stored in
   the Xibo dataset.

:program:`Meetup2Xibo` is a command line program that retrieves event
descriptions from Meetup.com and loads them into a Xibo digital signage
dataset.
Xibo layouts can contain ticker widgets that filter, sort, and display event
data.
:numref:`Figure %s <meetup2xibo-event-data-flow>` shows event data flow from
Meetup.com to Xibo layouts.

Installation
------------

Meetup2Xibo can be installed with standard Python package tools.
See :doc:`installation`.

Configuration
-------------

Meetup2Xibo gets its configuration from environment variables.
The configuration includes:

- Meetup.com API credentials
- Xibo CMS API credentials
- Xibo dataset column names
- Location corrections
- Date/time thresholds for event insertion, deletion, and cancellation

The :ref:`meetup2xibo man page <meetup2xibo-environment>` defines the
configuration environment variables.
An annotated example configuration script provides a starting point for
customization.

Logging
-------

Meetup2Xibo can log its activity to a named file, standard output, or both.
:ref:`Command line options <meetup2xibo-options>` control the message levels to
log and where to send the logs.

A supporting program, :program:`summarize-m2x-logs`, analyzes logs and
summarizes changes to events.
See the :doc:`man page </man/summarize-m2x-logs>`.

Cron Jobs
---------

The Linux cron daemon (or the Windows Task Scheduler) can run 
Cron runs meetup2xibo every 10 minutes so the Xibo layouts show the latest
event changes, particularly last minute room changes.
Cron runs summarize-m2x-logs early every morning to mail a summary of the
previous days logs.


