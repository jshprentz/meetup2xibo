========
Overview
========

.. figure:: /images/diagrams/meetup2xibo-event-data-flow.png
   :alt: Diagram showing the event data flow from Meetup.com to Xibo
   :name: meetup2xibo-event-data-flow
   :align: center

   Meetup2xibo retrieves event data from Meetup.com, transforms the data, and
   updates the event data stored in a Xibo dataset.
   Ticker widgets in Xibo layouts display the event data retrieved from
   the Xibo dataset.

:program:`Meetup2xibo` is a command line program that retrieves event
descriptions from Meetup.com and loads them into a Xibo digital signage
dataset.
Xibo layouts can contain ticker widgets that filter, sort, and display event
data.
:numref:`Figure %s <meetup2xibo-event-data-flow>` shows event data flow from
Meetup.com to Xibo layouts.

Preparation
-----------

Meetup2xibo run on any computer running Linux or a similar operating system.
An administrator will need some basic computer skills to install and configure
meetup2xibo.
See :doc:`prerequisites` for a description of the computing and skills
requirements.

Meetup2xibo stores event data in a Xibo dataset.
See :doc:`xibo-quick-start` for instructions about about importing the dataset
structure and an agenda layout.
Alternatively, see :doc:`xibo-dataset-setup` for instructions about creating
the dataset manually.

Meetup2xibo accesses the Xibo API as a distinct authorized user.
See :doc:`xibo-user-setup` for instructions about adding and authorizing this
user.

Installation
------------

Meetup2xibo can be installed with standard Python package tools.
See :doc:`installation`.

Configuration
-------------

Meetup2xibo gets its configuration from environment variables.
The configuration includes:

- Meetup.com API settings
- Xibo CMS API credentials
- Xibo dataset column names
- Location corrections
- Places for schedule conflict analysis
- Date/time thresholds for event insertion, deletion, and cancellation

The :ref:`meetup2xibo man page <meetup2xibo-environment>` defines the
configuration environment variables.
:doc:`configuration` explains the environment variables in more detail.
An annotated example configuration script, :github-raw:`/data/meetup2xibo.env`,
provides a starting point for customization.

Logging
-------

Meetup2xibo can log its activity to a named file, standard output, or both.
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
Cron runs summarize-m2x-logs early every morning to email a summary of the
previous days logs.
See :doc:`cron-jobs` for instructions about setting up the cron jobs.

