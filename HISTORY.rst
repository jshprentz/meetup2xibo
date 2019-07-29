=======
History
=======

~~~~~~~~~~~~~~
Future History
~~~~~~~~~~~~~~

* Support Xibo 2.
* Improve reporting of JSON configuration errors.

~~~~~~~~~~~~~~
Recent History
~~~~~~~~~~~~~~

.. Next Release
.. ------------------

3.2.0 (2019-07-29)
------------------
* Document quick start import of dataset structure.

3.1.0 (2019-07-27)
------------------
* Meetup API key no longer is sent to Meetup.com.
* Environment variable ``MEETUP_API_KEY`` may be removed from configurations.

3.0.1 (2019-07-27)
------------------
* Document logging and reporting schedule conflicts.
* Fix documentation issues.


3.0.0 (2019-07-25)
------------------
* Detect and report room conflicts.

2.4.10 (2019-06-12)
-------------------
* Report reversion to earlier unknown locations in log summaries.
* Improve reporting of OAuth2 errors.

2.4.9 (2019-05-30)
------------------
* Improve reporting of Xibo dataset discovery errors.

2.4.8 (2019-05-29)
------------------
* Improve reporting of Meetup.com server errors.
* Add Python 3.7 tests to Travis CI.
* Change development status from beta to production.

2.4.7 (2019-05-27)
------------------
* Add missing modules to distribution manifest.

2.4.6 (2019-05-27)
------------------
* First release on PyPI.
* Document location conversion spreadsheet

2.4.5 (2019-05-26)
------------------
* Complete user manual.

2.4.4 (2019-05-25)
------------------
* Expand documentation.
* Test with Python 3.7 also.

2.4.3 (2019-05-08)
------------------
* Add documentation.

2.4.2 (2019-04-25)
------------------
* Correct conversion of cancelled events.
* Add man pages to documentation.

2.4.1 (2019-03-26)
------------------
* Ignore "3D" accounting code in event names.
* Summarize past and current changes in separate lists.

2.4.0 (2019-03-21)
------------------
* Report event updates with human-friendly field names (e.g., start time instead of start_time).
* Add TIMEZONE environment property.
* Make Meetup to Xibo event conversions timezone aware.

2.3.2 (2019-03-18)
------------------
* Correct filename travis.yml to .travis.yml.

2.3.1 (2019-03-18)
------------------
* Add Travis CI configuration.

2.3.0 (2019-03-18)
------------------
* Summarize location mappings in CSV format.
* Describe past deleted events as "retired."
* Improve email header generation.

2.2.2 (2019-03-15)
------------------
* Add configuration parameter for the number of Meetup events to request.
* Improve reporting of HTTP errors.

2.2.1 (2019-03-14)
------------------
* Add special locations no longer needed to log summary reports.
* Improve formatting of log summary reports.
* Move xibo_id to end of XiboEvent tuples to ease visual comparison with PartialEvent tuples in logs.

2.2.0 (2019-03-13)
------------------
* Add comand line arguments to log summarizer: input, output, email headers.
* Add yesterday script.
* Simplify all times to HH:MM, omitting seconds.
* Report unknown location warnings.

2.1.0 (2019-03-13)
------------------
* Add tools to summarize meetup2xibo logs

2.0.1 (2019-03-06)
------------------
* Improve location analysis and overrides.
* Track cancelled events.
* Add documentation with Sphinx and ReadTheDocs.
* Replace MySQL access with Xibo web API.
* Replace Python configuration file with environment based configuration.
* Restructure code with dependency injection.
* Add Python package support.
* Reformat to conform to PEP-8.
* Test with multiple Python versions (3.5 and 3.6).

~~~~~~~~~~~~~~~
Ancient History
~~~~~~~~~~~~~~~

1.0.1 (2017-12-12)
------------------

* Download events from Meetup web API.
* Insert/update/delete corresponding Xibo events directly in Xibo's MySQL database.
