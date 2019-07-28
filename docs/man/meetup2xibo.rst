meetup2xibo
===========

Synopsis
--------

**meetup2xibo** [-h] [-d] [-l <*LOGFILE*>] [-c] [-m] [-v] [-w]

Description
-----------

:program:`meetup2xibo` downloads events from Meetup.com and updates the
corresponding events stored in a Xibo CMS dateset.

:program:`meetup2xibo` reads its configuration from
:ref:`environment variables <meetup2xibo-environment>`.
The :ref:`command line options <meetup2xibo-options>` control only
the message levels to log and where to send the logs.

.. _meetup2xibo-options:

Options
-------

.. program:: meetup2xibo

.. option:: -h, --help

   Show a help message and exit.

.. option:: -d, --debug

   Also log debug messages. If this option is omitted,
   log only info and higher level messages.

.. option:: -l <LOGFILE>, --logfile <LOGFILE>

   Path to logfile (default: meetup2xibo.log).

.. option:: -c, --conflicts

   Log conflict detection details about Meetup events and the places where they
   are scheduled.
   Default: do not log conflict details.

   .. versionadded:: 3.0

.. option:: -m, --mappings

   Log location mappings from Meetup.com's venue name and find-us fields
   to Xibo's location field.
   Default: log mappings only with debug messages.

.. option:: -v, --verbose

   Log to standard error.
   This is useful for debugging when running from the command line.

.. option:: -w, --warnings

   Log warnings and higher level messages to standard error.
   This is useful when running in cron job because cron
   will mail any standard error output.

.. _meetup2xibo-environment:

Environment
-----------

.. envvar:: CONFLICT_PLACES

   A JSON array of places to check for scheduling conflicts.

   .. versionadded:: 3.0

.. envvar:: CONTAINED_PLACES

   A JSON array of objects showing a place and the other places it contains
   For example::

    export CONTAINING_PLACES='[
        {"place": "Ballroom", "contains": ["North Ballroom", "South Ballroom"]},
        {"place": "Ballroom Suite", "contains": ["Ballroom", "Dressing Room"]},
    ]'

   .. versionadded:: 3.0

.. envvar:: DEFAULT_LOCATION

   The location to store in Xibo when Meetup's venue name and find-us fields
   contain no recognizable locations.

.. envvar:: DEFAULT_PLACES

   A JSON array of places associated with the default location.

   .. versionadded:: 3.0

.. envvar:: DELETE_AFTER_END_HOURS

   The number of hours after an event ends to wait before retiring the event
   from Xibo.

.. envvar:: DELETE_BEFORE_START_HOURS

   The number of hours before an event starts required to delete from Xibo an
   event not listed by Meetup.

.. envvar:: DELETE_UNTIL_FUTURE_DAYS

   The number of days in the future when an event not listed by Meetup may be
   deleted from Xibo.

.. envvar:: END_TIME_COLUMN_NAME

   The name of the Xibo dataset column containing event end times in `ISO 8601`_ format.

.. _ISO 8601: https://xkcd.com/1179/

.. envvar:: EVENT_DATASET_CODE

   The API code assigned to the Xibo event dataset.

.. envvar:: IGNORE_CANCELLED_AFTER_DAYS

   The number of days in the future to ignore cancelled events and quietly
   delete them from Xibo.

.. envvar:: LOCATION_COLUMN_NAME

   The name of the Xibo dataset column containing event locations.

.. envvar:: MEETUP_API_KEY

   The API key that authenticates access to Meetup.com.

.. deprecated:: 3.1
   The Meetup API key no longer is sent to Meetup.com.
   This environment variable may be removed from configurations.

.. envvar:: MEETUP_EVENTS_WANTED

   The number of events to request from Meetup.

.. envvar:: MEETUP_GROUP_URL_NAME

   The group name for Meetup URLs.
   For example, in the URL https://www.meetup.com/NOVA-Makers/,
   the group name is *NOVA-Makers*.

.. envvar:: MEETUP_ID_COLUMN_NAME

   The name of the Xibo dataset column containing Meetup event IDs.

.. envvar:: MORE_PLACE_PHRASES

   A second list of phrases and places to try if :envvar:`PLACE_PHRASES`
   failed to match.
   See :envvar:`PLACE_PHRASES` for the JSON format.

   .. versionchanged:: 3.0
      Was ``MORE_LOCATION_PHRASES`` with a different format.     

.. envvar:: NAME_COLUMN_NAME

   The name of the Xibo dataset column containing event names.

.. envvar:: PLACE_PHRASES

   A JSON array of objects containing a phrase to match and a corresponding
   place. For example::

    export PLACE_PHRASES='[
       {"phrase": "Conf Rm 1",          "place": "Conference Room 1"},
       {"phrase": "Conf Rm 2",          "place": "Conference Room 2"},
       {"phrase": "Conference room 1",  "place": "Conference Room 1"},
       {"phrase": "Conference room 2",  "place": "Conference Room 2"}
    ]'

   .. versionchanged:: 3.0
      Was ``LOCATION_PHRASES`` with a different format.     

.. envvar:: SITE_CA_PATH

   The optional path to a self-signed certificate for Xibo.

.. envvar:: SPECIAL_LOCATIONS

   A JSON array of objects that correct or override missing, incorrect, or
   verbose event locations from Meetup.
   For example::

    export SPECIAL_LOCATIONS='[
        {"meetup_id": "zvbxrpl2", "location": "Orange Bay",
	 "comment": "", "override": false, "places": ["Orange Bay"]},
        {"meetup_id": "lrzzfbhb", "location": "Private",
	 "comment": "Private meeting", "override": true, "places": []}
    ]'

   List *meetup_id* to suppress warnings about missing locations.
   A non-blank *location* replaces the default location and can replace the
   computed location.
   Any *comment* helps document the special location.
   When true, the *override* flag forces a non-blank location to replace the
   computed location.
   Conflict resolution examines the list of *places* associated with the
   location.

   .. versionchanged:: 3.0
      Added *places.*

.. envvar:: START_TIME_COLUMN_NAME

   The name of the Xibo dataset column containing event start times in `ISO 8601`_ format.

.. envvar:: TIMEZONE

   The timezone database name of the timezone configured in Xibo.
   For example, ``America/New_York``.
   See the `list of timezones`_ for timezone database names.
   
.. _list of timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

.. envvar:: XIBO_CLIENT_ID

   The client ID that identifies this application to Xibo.

.. envvar:: XIBO_CLIENT_SECRET

   The client secret that authenticates this application to Xibo.

.. envvar:: XIBO_HOST

   The hostname or IP address of the Xibo CMS server.

.. envvar:: XIBO_ID_COLUMN_NAME

   The name of the Xibo dataset column containing Xibo event IDs.

.. envvar:: XIBO_PORT

   The port number of the Xibo CMS server, usually 443.
