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

.. warning::

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

   The Meetup.com group URL name, circled in red, is the last part of the
   group's Meetup.com URL.
   
Xibo CMS API Credentials
------------------------

Xibo Dataset Column Names
-------------------------

Location Corrections
--------------------

Date/time Thresholds
--------------------


.. _`Getting an API Key`: https://secure.meetup.com/meetup_api/key/
.. _`The Twelve-Factor App`: https://12factor.net/config
