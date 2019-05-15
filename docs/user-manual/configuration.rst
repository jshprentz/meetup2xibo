=============
Configuration
=============

As recommended in `The Twelve-Factor App`_,
meetup2xibo gets its configuration from environment variables.
The :ref:`meetup2xibo man page <meetup2xibo-environment>` defines the
configuration environment variables.
The configuration includes:

- Meetup.com :abbr:`API(application programming interface)` credentials
- Xibo :abbr:`CMS(Content Management System)` API credentials
- Xibo dataset column names
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

Meetup.com API Credentials
--------------------------

Meetup.com requires an API key with each request.
The API key identifies and authenticates the user of the client application
(meetup2xibo in this case).
Meetup.com issues API keys on their `Getting an API Key`_ web page.
Environment variable :envvar:`MEETUP_API_KEY` provides the API key.

.. note::

   Meetup.com announced that they will issue no new API keys.
   They prefer OAuth2, a more secure authentication system.
   Meetup2xibo needs revision to support OAuth2 at Meetup.com. 

Meetup2xibo requests events for a specific Meetup.com group.
The Meetup.com API use a computer-friendly group :abbr:`URL(Uniform Resource
Locator)` name instead of the actual group name.
Locate the group URL name in a web browser address line as shown in
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
The environment variables :envvar:`XIBO_CLIENT_ID` and
:envvar:`XIBO_CLIENT_SECRET` provide the necessary credentials.

Xibo Dataset Column Names
-------------------------

environment variable :envvar:`EVENT_DATASET_CODE`
environment variable :envvar:`MEETUP_ID_COLUMN_NAME`
environment variable :envvar:`NAME_COLUMN_NAME`
environment variable :envvar:`LOCATION_COLUMN_NAME`
environment variable :envvar:`START_TIME_COLUMN_NAME`
environment variable :envvar:`END_TIME_COLUMN_NAME`
environment variable :envvar:`XIBO_ID_COLUMN_NAME`
environment variable :envvar:`TIMEZONE`

Location Corrections
--------------------

Date/time Thresholds
--------------------


.. _`Getting an API Key`: https://secure.meetup.com/meetup_api/key/
.. _`The Twelve-Factor App`: https://12factor.net/config
