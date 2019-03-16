=======
History
=======

2.3 (Future)
------------------

* First release on PyPI.

Next Release
------------------

2.2.2 (2019-03-15)
------------------
* Add log summarizer configuration parameter for the number of Meetup events to request.
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

1.0.1 (2017-12-12)
------------------

* Download events from Meetup web API.
* Insert/update/delete corresponding Xibo events directly in Xibo's MySQL database.
