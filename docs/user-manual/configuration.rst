=============
Configuration
=============

As recommended in `The Twelve-Factor App`_,
meetup2xibo gets its configuration from environment variables.
The :ref:`meetup2xibo man page <meetup2xibo-environment>` defines the
configuration environment variables.
The configuration includes:

- Meetup.com :abbr:`API(application programming interface)` settings
- Xibo :abbr:`CMS(Content Management System)` API credentials
- Xibo dataset code and column names
- Xibo web server certificate
- Location corrections
- Date/time thresholds for event insertion, deletion, and cancellation

On Linux, a configuration shell script is a common way to provide environment
variables.
An annotated example configuration script, :github-raw:`/data/meetup2xibo.env`,
provides a starting point for customization.

The configuration script includes sensitive authorization data, so limit access
to the user running meetup2xibo.
For example, this chmod command gives the user read and write permissions, and
removes permissions from group members and other users:

.. code-block:: bash

   $ chmod u=rw,go-rwx meetup2xibo.env

Meetup.com API Settings
-----------------------

Meetup2xibo requests events for a specific Meetup.com group.
The Meetup.com API use a computer-friendly group :abbr:`URL(Uniform Resource
Locator)` name instead of the actual group name.
Locate the group URL name in a web browser address line, as shown in
:numref:`Figure %s <meetup-url-name>`.
Environment variable :envvar:`MEETUP_GROUP_URL_NAME` provides the URL group
name.

.. figure:: /images/screenshots/meetup-url-name.png
   :alt: Screenshot of a web browser address line with the Meetup.com URL group
         name circled within the URL
   :name: meetup-url-name
   :align: center

   The Meetup.com group URL name, "NOVA-Makers" circled in red, is the last
   part of the group's Meetup.com URL.

By default, the Meetup.com API returns data about the next 200 upcoming events.
During 2018 at Nova Labs, this provided about 60 days of future events.
By mid-2019, 200 upcoming events provided only 45 days of future events.

Organizations with more or fewer events may want data about more or fewer than
200 upcoming events.
Rather than rely on the Meetup.com default, environment variable
:envvar:`MEETUP_EVENTS_WANTED` specifies the number of upcoming events wanted
from Meetup.com.

.. _`xibo-cms-api-credentials`:

Xibo CMS API Credentials
------------------------

Meetup2xibo connects to the Xibo CMS running on the host specified by
environment variable :envvar:`XIBO_HOST`.
This value may be an IP address, a hostname, or a domain name.
Meetup2xibo does not need to run on the same computer as the Xibo CMS.

Meetup2xibo connects to the port number specified by environment variable
:envvar:`XIBO_PORT`.
The standard SSL/HTTPS port is number 443.

The Xibo CMS authenticates client applications with OAuth2.
The client application, meetup2xibo, needs a client ID and a client secret.
When a Xibo administrator adds or edits an application, Xibo reveals the client
ID and client secret as described in :ref:`authorize-the-application` and shown
in :numref:`Figure %s <edit-application-general>`.
The environment variables :envvar:`XIBO_CLIENT_ID` and
:envvar:`XIBO_CLIENT_SECRET` provide the necessary credentials to meetup2xibo.

.. _`xibo-dataset-config`:

Xibo Dataset Code and Column Names
----------------------------------

The Xibo administrator creates an events dataset through the Xibo CMS web
interface as described in :ref:`create-an-events-dataset`.
The administrator chooses a code to identify the dataset for Xibo
API clients, as shown in :numref:`Figure %s <add-dataset-dialog>`.
Configure the code in environment variable :envvar:`EVENT_DATASET_CODE`.

The Xibo administrator creates dataset columns and assigns column headings as
described in :ref:`dataset_columns`.
Those column headings must be configured in environment variables for
meetup2xibo.
:numref:`Table %s <column_env_vars>` lists the environment variables and their
corresponding column headings at Nova Labs.
Use the column headings chosen in :ref:`dataset_columns`.
Environment variable :envvar:`XIBO_ID_COLUMN_NAME` must have the value *id,*
the heading assigned internally by the Xibo CMS.

.. tabularcolumns:: |L|L|

.. _column_env_vars:

.. table:: Environment Variables for Dataset Columns
   :align: center

   +----------------------------------+----------------+
   | Environment Variable             | Column Heading |
   +==================================+================+
   | :envvar:`MEETUP_ID_COLUMN_NAME`  | Meetup ID      |
   +----------------------------------+----------------+
   | :envvar:`NAME_COLUMN_NAME`       | Name           |
   +----------------------------------+----------------+
   | :envvar:`LOCATION_COLUMN_NAME`   | Location       |
   +----------------------------------+----------------+
   | :envvar:`START_TIME_COLUMN_NAME` | ISO Start Time |
   +----------------------------------+----------------+
   | :envvar:`END_TIME_COLUMN_NAME`   | ISO End Time   |
   +----------------------------------+----------------+
   | :envvar:`XIBO_ID_COLUMN_NAME`    | id             |
   +----------------------------------+----------------+

Xibo Web Server Certificate
---------------------------

An :abbr:`SSL (Secure Sockets Layer)` certificate secures Xibo's web servers.
A certificate may be purchased from a certificate authority, a web hosting
company, or another provider.
`Let's Encrypt`_ provides free certificates through its automated web site.

Meetup2xibo's implementation language, Python, recognizes SSL certificates
issued by major certificate authorities, including Let's Encrypt..
Meetup2xibo needs no configuration to support these SSL certificates.

Some Xibo installations must rely on self-signed SSL certificates to provide
secure access.
Digital Ocean has a helpful guide for setting this up:
`How To Create a Self-Signed SSL Certificate for Apache in Ubuntu 16.04`_.

When a self-signed certificate protects Xibo's web server, meetup2xibo needs
the path to the certificate's public key configured by environment variable
:envvar:`SITE_CA_PATH`.

Location Corrections
--------------------

Meetup.com provides many details about meeting venues: name, street address,
city, state, country, latitude, longitude, and more.
Meetup.com also provides a "how to find us" data field.
Most Nova Labs events take place inside Nova Labs, so the agenda displays only
the name of the classroom, conference room, or workshop.
The Meetup.com venue name and how-to-find-us fields usually contain the room
assignment(s), among other information.

Meetup2xibo scans the venue name and "how to find us" fields, searching for
known places, such as rooms, workshops, studios, classrooms, fields, etc.
The places are collected in the order found.
Meetup2xibo corrects place spelling variations and renders the list as an
English phrase such as "Room 1, Room 2, and Workshop 3."
The resulting phrase is stored in the Xibo events dataset location field.

For example, a woodworking class has the venue name "\*Nova Labs (Conference Rm
2)" and the how-to-find-us "[woodshop]".
Meetup.com sets the location in Xibo to "Conference Room 2 and Woodshop".

Place Phrases
~~~~~~~~~~~~~

When scanning the venue name and "how to find us" fields, Meetup2xibo searches
for phrases provided in a curated list of phrases and preferred place names.
For example, :numref:`Table %s <example_phrases_and_places>` shows the
phrases that match the preferred place name "Conference Room 1."

.. tabularcolumns:: |L|L|

.. _example_phrases_and_places:

.. table:: Example Phrases and Places
   :align: center

   +-------------------+-------------------+
   | Phrase            | Place             |
   +===================+===================+
   | Conf Rm 1         | Conference Room 1 |
   +-------------------+-------------------+
   | Conference rm 1   | Conference Room 1 |
   +-------------------+-------------------+
   | Conference room 1 | Conference Room 1 |
   +-------------------+-------------------+

The list of phrases and corresponding places is configured in environment
variable :envvar:`PLACE_PHRASES` as a
:abbr:`JSON (JavaScript Object Notation)` list of objects, as shown in
:numref:`Listing %s <place-phrases-config-example>`.

.. code-block:: bash
   :caption: Place Phrases JSON Configuration Example
   :name: place-phrases-config-example

   export PLACE_PHRASES='[
       {"phrase": "Conf Rm 1",         "place": "Conference Room 1"},
       {"phrase": "Conference rm 1",   "place": "Conference Room 1"},
       {"phrase": "Conference room 1", "place": "Conference Room 1"}
   ]'

Meetup2xibo ignores spacing and upper/lower case distinctions when searching
for phrases.
There is no need, for example, to list both "Conf Rm 1" and "Conf rm 1".

Meetup2xibo matches the longest possible phrases first, regardless of their
order in the configuration file.
For example, phrase "Room 123" would be matched ahead of phrases "Room 1" and
"Room 12".

If none of the phrases configured in environment variable
:envvar:`PLACE_PHRASES` match, Meetup2Xibo tries matching the phrases in
environment variable :envvar:`MORE_PLACE_PHRASES`.
The format is the same as shown in
:numref:`Listing %s <place-phrases-config-example>`.
At Nova Labs, :envvar:`PLACE_PHRASES` lists specific rooms within Nova Labs.
:envvar:`MORE_PLACE_PHRASES` lists more general event places, such as Nova
Labs; nearby event places, such as George Mason University; and the uncertain
:abbr:`TBD (To Be Determined)`.

Default Location
~~~~~~~~~~~~~~~~

If none of the place phrases match, Meetup2xibo uses the location specified
by environment variable :envvar:`DEFAULT_LOCATION`.
Meetup2xibo logs a warning message whenever the default location is needed.

To support :ref:`conflict detection <scheduling-conflicts>`, environment
variable :envvar:`DEFAULT_PLACES` lists places associated with the default
location.
:numref:`Listing %s <specific-default-location-example>` shows an example of
a default locaion associated with specific places.

.. code-block:: bash
   :caption: Default Location with Specific Places Example
   :name: specific-default-location-example

   export DEFAULT_LOCATION="Dance Studios"
   export DEFAULT_PLACES='["Studio 1", "Studio 2"]'

:numref:`Listing %s <general-default-location-example>` shows default location
and places at Nova Labs.
The default location does not identify any specific room or workshop, so the
default places list is empty.

.. code-block:: bash
   :caption: Default Location with No Specific Places Example
   :name: general-default-location-example

   export DEFAULT_LOCATION="Nova Labs"
   export DEFAULT_PLACES='[]'

Special Locations
~~~~~~~~~~~~~~~~~

Some Meetup.com events have missing, uncommon, or incorrect locations.
Environment variable :envvar:`SPECIAL_LOCATIONS` contains a list of JSON
objects that control the matching process for specific events.
:numref:`Listing %s <special-locations-config-example>` shows examples of
special locations.

.. code-block:: bash
   :caption: Special Locations JSON Configuration Example
   :name: special-locations-config-example
   :linenos:

   export SPECIAL_LOCATIONS='
   [
       {
           "meetup_id": "259083135",
           "location": "",
	   "places": [],
           "override": false,
           "comment": "Electronics 101: no room yet"
       },
       {
           "meetup_id": "gqpyzfbhb",
           "location": "Classroom A",
	   "places": ["Classroom A"],
           "override": false,
           "comment": "Location in event name"
       },
       {
           "meetup_id": "269568127",
           "location": "Baltimore Museum of Industry",
	   "places": [],
           "override": false,
           "comment": "Field trip"
       },
       {
           "meetup_id": "259565142",
           "location": "Parking Lot, Classroom A, and Conference Room 2",
	   "places": ["Classroom A", "Conference Room 2"],
           "override": true,
           "comment": "Picnic"
       }
   ]'

Within each special location object, the :mailheader:`meetup_id` contains the
event ID from Meetup.com.
The :mailheader:`location` contains the event location for Xibo.
The :mailheader:`location` may be an empty string if the meetup2xibo default
location is acceptable.
The :mailheader:`places` contains a list of places to check for conflicts.
The :mailheader:`override` flag must have a ``true`` or ``false`` value as
explained below.
The :mailheader:`comment` helps administrators remember why the special
location was created; it may be an empty string.
Missing location warnings are suppressed for events with special location
objects.

After the location matching process, meetup2xibo applies these rules to the
computed location:

-   For events with no special location object, prefer any computed location
    over the default.

-   For events with a special location object and no computed location, prefer
    any special location over the default.

-   For events with both a special location object and a computed location, if
    the :mailheader:`override` flag is ``true``, prefer any special location
    over the computed location over the default. Otherwise, if the
    :mailheader:`override` flag is ``false``, prefer the computed location over
    any special location over the default.

The following examples demonstrate the use of special locations:

No Meetup.com venue name or how-to-find-us
   Meetup2xibo will use the default location and log a warning.
   When the administrator adds the special location object shown in
   :numref:`Listing %s <special-locations-config-example>` lines 3--9,
   meetup2xibo will continue to use the default location and places without
   logging a warning.
   If the event host later adds a venue name or how-to-find-us in Meetup.com,
   meetup2xibo will use known locations found there instead of the default
   location.

Known location only in Meetup.com event name or description
   Meetup2xibo will use the default location and log a warning.
   When the administrator adds the special location object shown in
   :numref:`Listing %s <special-locations-config-example>` lines 10--16,
   meetup2xibo will use the special location instead of the default location.
   The place "Classroom A" will be checked for conflicts.
   If the event host later adds a venue name or how-to-find-us in Meetup.com,
   meetup2xibo will use known places found there instead of the special
   location or the default location.

Unknown locations from Meetup.com
   Meetup2xibo will use the default location and log a warning.
   When the administrator adds the special location object shown in
   :numref:`Listing %s <special-locations-config-example>` lines 17--23,
   meetup2xibo will use the special location and places instead of the default
   location and places.

Known and unknown locations from Meetup.com
   Meetup2xibo will derive a location from the known places found in the venue
   name or how-to-find-us, "Classroom A" and "Conference Room 2" in this
   example.
   Meetup2xibo will not recognize "Parking Lot," an uncommon and unconfigured
   place.
   When the administrator adds the special location object shown in
   :numref:`Listing %s <special-locations-config-example>` lines 24--30,
   meetup2xibo will use the special location and places, overriding the
   location derived from the known places.

.. _`scheduling-conflicts`:

Detecting Scheduling Conflicts
------------------------------

Meetup2xibo and summarize-m2x-logs can detect and report possible scheduling
conflicts.
A conflict occurs when two or more events are scheduled in the same place at
the same time.

Meetup2xibo checks for conflicts only in places listed by environment variable
:envvar:`CONFLICT_PLACES`.
Other places, such as an entire facility (Nova Labs) or a common gathering
area (Lobby), can accomodate multiple simultaneous activities.
:numref:`Listing %s <conflict-places-example>` shows an example of
a list of places with possible scheduling conflicts.

.. code-block:: bash
   :caption: Conflict Places Example
   :name: conflict-places-example

   export CONFLICT_PLACES='[
       "Classroom A",
       "Classroom A/B",
       "Classroom B",
       "Computer Lab",
       "Conference Room 1",
       "Conference Room 2",
       "Conference Room 3"
   ]'

Some places may be subdivided; others may be combined.
For example, Classroom A/B may be partitioned into Classroom A and Classroom B.
Conferences Rooms 1, 2, and 3 may be combined to form the Conference Center.
Meetup2xibo must know which places contain other places to detect scheduling
conflicts such as simultaneous meetings in Classroom A and Classroom A/B.

Environment variable :envvar:`CONTAINED_PLACES` lists JSON objects describing
places containing other places.
:numref:`Listing %s <contained-places-example>` shows the example above of
Classroom A/B and the Conference Center.

.. code-block:: bash
   :caption: Contained Places Example
   :name: contained-places-example

    export CONTAINING_PLACES='[
        {"place": "Classroom A/B",
         "contains": ["Classroom A", "Classroom B"]},
        {"place": "Conference Center",
         "contains": ["Conference Room 1", "Conference Room 2", "Conference Room 3"]}
    ]'

Meetup2xibo supports typical facilities with few restrictions.

Places may be listed in any order.
   Places are analyzed by name, not by their position in lists.

Contained places may be nested.
   For example, the Convention Center may contain the Conference Center among
   other places.

Contained places may overlap.
   A Seminar Area may contain Classroom A and Conference 1, overlapping the
   example places Classroom A/B and Conference Center.

Contained and containing places need not be checked for conflicts.
   For example, the Conference Center is not on the list of ``CONFLICT_PLACES``.

Loops are forbidden.
   The Conference Center may not contain the Convention Center if the
   Convention Center already contains the Conference Center.

Timezone
--------

Meetup2xibo converts event start and end times from :abbr:`UTC (Coordinated
Universal Time)`, the internal format of Meetup.com, to the timezone configured
in the Xibo CMS.
:numref:`Figure %s <regional-settings>` shows how to review or change the Xibo
timezone.

.. figure:: /images/screenshots/regional-settings.png
   :alt: Screenshot of the Xibo regional settings 
   :name: regional-settings
   :align: center

   Click :guilabel:`Settings` (1) in the Xibo CMS menu to display some of
   Xibo's settings.
   Click the :guilabel:`Regional` tab (2) to display settins that vary by
   region.
   Review or change the timezone (3) using the dropdown menu.
   Click the :guilabel:`Save` button (4) to save changes, if necessary.

The timezone specified by environment variable :envvar:`TIMEZONE` must
correspond to the setting in Xibo, but the format is slightly different.
Meetup2xibo follows the `naming rules for the tz database
<tz-database-naming-rules>`_.
Wikipedia provides a convenient `List of tz database time zones`_.
For example, Nova Labs, near Washington, DC, set the Xibo timezone to
"(GMT-04:00) America, New York" in August 2017, a daylight savings time month..
The corresponding tz database name is "America/New_York".

Date/time Thresholds
--------------------

The Meetup.com API sometimes fails to list current and very recent events while
Xibo still should display them.
Events in the Xibo dataset and missing from Meetup.com should not be deleted
unless they start some number of hours in the future, configured by environment
variable :envvar:`DELETE_BEFORE_START_HOURS`.

Some Xibo displays, such as daily agendas and weekly calendars, should continue
to display events after their conclusion.
Past events should not be delegted from the Xibo dataset until some number of
hours after they end, as configured by environment variable
:envvar:`DELETE_AFTER_END_HOURS`.

The Meetup.com API lists some fixed number (hundreds) of future events.
As new near-term events are added to the Meetup.com calendar, some previously
reported far future events are bumped from the listing.
To avoid flapping, meetup2xibo does not delete events from the Xibo dataset
more than some number of days in the future, as configured by environment
variable :envvar:`DELETE_UNTIL_FUTURE_DAYS`.

When Meetup.com events are cancelled far in the future, guests have ample time
to receive notifications and alter thier plans.
Meetup2xibo ignores cancelled events after some number of days in the future,
configured by environment variable :envvar:`IGNORE_CANCELLED_AFTER_DAYS`,
treating them as deleted.

.. _`Getting an API Key`: https://secure.meetup.com/meetup_api/key/
.. _`How To Create a Self-Signed SSL Certificate for Apache in Ubuntu 16.04`: https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-16-04
.. _`Let's Encrypt`: https://letsencrypt.org/
.. _`List of tz database time zones`: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
.. _`tz-database-naming-rules`: https://en.wikipedia.org/wiki/Tz_database#Names_of_time_zones
.. _`The Twelve-Factor App`: https://12factor.net/config
