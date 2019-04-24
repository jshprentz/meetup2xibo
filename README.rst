.. Use only basic Restructured Text in this file so PyPi and GitHub can display it.
.. No Sphinx extensions here.

==============
Meetup to Xibo
==============


.. image:: https://img.shields.io/travis/jshprentz/meetup2xibo.svg
        :target: https://travis-ci.org/jshprentz/meetup2xibo

.. image:: https://readthedocs.org/projects/meetup2xibo/badge/?version=latest
        :target: https://meetup2xibo.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. Start description

**Meetup2xibo** is a command line program that retrieves event descriptions
from Meetup.com and loads them into a Xibo digital signage dataset.
Xibo can display events in sign layouts such as agendas, calendars, room
activity signs, and maps.

Meetup2xibo was developed for `Nova Labs`_, a makerspace in Reston, Virginia.
The busy Nova Labs calendar has up to a dozen Meetup.com events per day.
Xibo displays event agendas for today and tommorrow on several large
wall-mounted monitors.
Meetup2xibo keeps those agendas up-to-date as events are added, cancelled, or updated.

.. _`Nova Labs`: https://www.nova-labs.org/

.. PyPi requires an absolute image URL.
.. image:: https://raw.githubusercontent.com/jshprentz/meetup2xibo/development/docs/images/screenshots/calendar-to-agenda.png
	:alt: Diagram of meetup2xibo's function showing events from a
		screenshot of a Meetup.com calendar transformed
		into events displayed by Xibo in a daily agenda.

.. End description

* Documentation: https://meetup2xibo.readthedocs.io.
* GitHub: https://github.com/jshprentz/meetup2xibo
* Free software: MIT license


Features
--------

* Retrieves events from the Meetup.com API.
* Inserts, updates, and deletes events via the Xibo CMS API.
* Logs changes to Xibo events.
* Extracts event locations from Meetup.com venue name and find-us fields.
* Maps abbreviated and misspelled event locations to preferred forms.
* Allows per-event overrides of location mapping rules.
* Logs location mappings.
* Converts Meetup.com event start and end times into ISO 8601 local date/times for Xibo.
* Summarizes logs in a daily email message.

Credits
-------

**Meetup2xibo** was developed by Joel Shprentz (`@jshprentz`_).

.. _`@jshprentz`: https://github.com/jshprentz
